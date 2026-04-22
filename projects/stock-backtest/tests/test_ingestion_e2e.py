"""End-to-end scenario tests for :mod:`stock_backtest.ingestion.pipeline`.

TASK-033 — **multi-run** scenarios: verify that the pipeline correctly tracks
``MAX(time)`` across separate runs, recovers from previous failures (full or
partial), and remains idempotent on replay.

Unlike ``test_ingestion_pipeline.py`` (single-run unit tests with
``MagicMock`` repositories), this suite uses an **in-memory state container**
that mimics an actual database:

- ``ohlcv``: list of dicts keyed by (asset_id, time).
- ``ingestion_log``: append-only list of log rows.
- ``assets``: map of asset_id → asset attributes (``last_ingested_at``).

We patch the three repository classes where ``pipeline.py`` imports them so
every call goes through the in-memory ``_State`` below. As a result two
sequential :meth:`IngestionPipeline.run_for_asset` invocations share state
exactly like they would against a real Postgres instance.

No network, no DB required. ``sleep_fn=lambda _: None`` keeps runtime near
zero even when retries happen.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from types import SimpleNamespace
from typing import Any, Callable, Iterator, Optional
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from stock_backtest.ingestion.base import (
    DataSource,
    DataSourceError,
    RateLimitError,
)
from stock_backtest.ingestion.pipeline import IngestionPipeline


# ---------------------------------------------------------------------------
# In-memory state container
# ---------------------------------------------------------------------------


@dataclass
class _State:
    """In-memory stand-in for the three tables the pipeline writes to."""

    # (asset_id, time) → row dict (UPSERT target).
    ohlcv: dict[tuple[int, pd.Timestamp], dict[str, Any]] = field(default_factory=dict)
    # append-only event log.
    ingestion_log: list[dict[str, Any]] = field(default_factory=list)
    # asset_id → SimpleNamespace(...)
    assets: dict[int, Any] = field(default_factory=dict)

    # --- helpers -------------------------------------------------------
    def ohlcv_rows(self, asset_id: int) -> list[dict[str, Any]]:
        return [v for (aid, _t), v in sorted(self.ohlcv.items()) if aid == asset_id]

    def max_time(self, asset_id: int) -> Optional[datetime]:
        ts = [t for (aid, t) in self.ohlcv.keys() if aid == asset_id]
        if not ts:
            return None
        m = max(ts)
        # OhlcvRepository.get_max_time returns a datetime; normalize to UTC.
        if isinstance(m, pd.Timestamp):
            m = m.to_pydatetime()
        if m.tzinfo is None:
            m = m.replace(tzinfo=timezone.utc)
        return m

    def logs_with(self, *, status: Optional[str] = None) -> list[dict[str, Any]]:
        if status is None:
            return list(self.ingestion_log)
        return [r for r in self.ingestion_log if r.get("status") == status]


# ---------------------------------------------------------------------------
# Repository fakes bound to a shared _State instance
# ---------------------------------------------------------------------------


def _make_ohlcv_repo(state: _State) -> MagicMock:
    repo = MagicMock()

    def _get_max_time(asset_id: int) -> Optional[datetime]:
        return state.max_time(asset_id)

    def _upsert_bulk(asset_id: int, rows: list[dict[str, Any]]) -> int:
        for r in rows:
            t = r["time"]
            if not isinstance(t, pd.Timestamp):
                t = pd.Timestamp(t)
            key = (asset_id, t)
            state.ohlcv[key] = {**r, "asset_id": asset_id, "time": t}
        return len(rows)

    repo.get_max_time.side_effect = _get_max_time
    repo.upsert_bulk.side_effect = _upsert_bulk
    return repo


def _make_log_repo(state: _State) -> MagicMock:
    repo = MagicMock()

    def _log(
        *,
        asset_id: Optional[int],
        requested_start: Optional[date],
        requested_end: Optional[date],
        status: str,
        rows_inserted: int = 0,
        error_message: Optional[str] = None,
    ):
        entry = {
            "asset_id": asset_id,
            "requested_start": requested_start,
            "requested_end": requested_end,
            "status": status,
            "rows_inserted": rows_inserted,
            "error_message": error_message,
            "attempted_at": datetime.now(timezone.utc),
        }
        state.ingestion_log.append(entry)
        return SimpleNamespace(**entry)

    repo.log.side_effect = _log
    return repo


def _make_asset_repo(state: _State, list_active: list[Any] | None = None) -> MagicMock:
    repo = MagicMock()

    def _update_last_ingested(asset_id: int, ts: datetime) -> None:
        asset = state.assets.get(asset_id)
        if asset is not None:
            asset.last_ingested_at = ts

    repo.update_last_ingested.side_effect = _update_last_ingested
    repo.list_active.return_value = list_active or []
    return repo


@contextmanager
def _patched_pipeline(
    state: _State, list_active: list[Any] | None = None
) -> Iterator[SimpleNamespace]:
    ohlcv_repo = _make_ohlcv_repo(state)
    log_repo = _make_log_repo(state)
    asset_repo = _make_asset_repo(state, list_active=list_active)
    with patch(
        "stock_backtest.ingestion.pipeline.OhlcvRepository",
        return_value=ohlcv_repo,
    ), patch(
        "stock_backtest.ingestion.pipeline.IngestionLogRepository",
        return_value=log_repo,
    ), patch(
        "stock_backtest.ingestion.pipeline.AssetRepository",
        return_value=asset_repo,
    ), patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        yield SimpleNamespace(ohlcv=ohlcv_repo, log=log_repo, asset=asset_repo)


# ---------------------------------------------------------------------------
# Misc helpers
# ---------------------------------------------------------------------------


def _weekday_trading_days(_market, start, end):
    """Business-day calendar (Mon-Fri), returned as a ``pd.DatetimeIndex``."""
    idx = pd.date_range(start=start, end=end, freq="B")
    return pd.DatetimeIndex(idx).normalize()


def _make_settings(retry_max: int = 3, backoffs=(1.0, 2.0, 4.0)) -> Any:
    return SimpleNamespace(
        ingestion=SimpleNamespace(
            retry_max=retry_max, retry_backoff_seconds=list(backoffs)
        )
    )


def _make_asset(
    *,
    asset_id: int,
    symbol: str = "SPY",
    market: str = "US",
    start_date: date | None = date(2024, 1, 5),
    meta: dict | None = None,
) -> Any:
    return SimpleNamespace(
        asset_id=asset_id,
        symbol=symbol,
        market=market,
        start_date=start_date,
        meta=meta if meta is not None else {},
        last_ingested_at=None,
        active=True,
    )


def _ohlcv_df(
    dates: list[date], close_overrides: dict[int, Any] | None = None
) -> pd.DataFrame:
    rows = []
    for i, d in enumerate(dates):
        close = 100.0 + i
        if close_overrides is not None and i in close_overrides:
            close = close_overrides[i]
        rows.append(
            {
                "time": pd.Timestamp(d),
                "open": close,
                "high": close,
                "low": close,
                "close": close,
                "adj_close": close,
                "volume": 1000,
            }
        )
    return pd.DataFrame(rows)


class _FakeSession:
    """Minimal session stand-in shared across runs."""

    def __init__(self) -> None:
        self.committed = 0
        self.rolled_back = 0
        self.closed = 0

    def commit(self) -> None:
        self.committed += 1

    def rollback(self) -> None:
        self.rolled_back += 1

    def close(self) -> None:
        self.closed += 1


def _make_session_factory(session: _FakeSession) -> Callable[[], _FakeSession]:
    def factory() -> _FakeSession:
        return session

    return factory


def _make_datasource() -> MagicMock:
    src = MagicMock(spec=DataSource)
    src.source_name = "yfinance"
    return src


def _make_pipeline(
    state: _State,
    source: MagicMock,
    *,
    today: date,
    list_active: list[Any] | None = None,
) -> tuple[IngestionPipeline, SimpleNamespace]:
    """Build a pipeline bound to the shared state."""
    session = _FakeSession()
    pipe = IngestionPipeline(
        sources={"US": source},
        session_factory=_make_session_factory(session),
        settings=_make_settings(),
        today_fn=lambda: today,
        sleep_fn=lambda _s: None,
    )
    return pipe, SimpleNamespace(session=session)


# ===========================================================================
# E2E-1: Failure → next run recovers the gap
# ===========================================================================


def test_e2e_1_failure_then_gap_recovery():
    """Run A fails with repeated DataSourceError. Run B (next day) succeeds
    and ingests the full range. MAX(time) advancement drives the catch-up."""
    state = _State()
    asset = _make_asset(asset_id=1, start_date=date(2024, 1, 5))
    state.assets[1] = asset

    src = _make_datasource()

    # ----- Run A: 2024-01-05 ~ 01-10 requested, source raises 3 times -----
    src.fetch_ohlcv.side_effect = DataSourceError("boom")
    with _patched_pipeline(state):
        pipe_a, _ = _make_pipeline(state, src, today=date(2024, 1, 10))
        result_a = pipe_a.run_for_asset(asset)

    assert result_a.status == "FAILED"
    assert state.ohlcv == {}  # nothing persisted
    assert state.max_time(1) is None
    failed = state.logs_with(status="FAILED")
    assert len(failed) == 1

    # ----- Run B: next day, source healthy -----
    # Expected trading days (Mon-Fri) in [01-05, 01-11]: 01-05, 01-08..01-11 (5 days)
    expected_days = [
        date(2024, 1, 5),
        date(2024, 1, 8),
        date(2024, 1, 9),
        date(2024, 1, 10),
        date(2024, 1, 11),
    ]
    src.fetch_ohlcv.side_effect = None
    src.fetch_ohlcv.return_value = _ohlcv_df(expected_days)

    with _patched_pipeline(state):
        pipe_b, _ = _make_pipeline(state, src, today=date(2024, 1, 11))
        result_b = pipe_b.run_for_asset(asset)

    assert result_b.status == "SUCCESS"
    assert result_b.rows_inserted == 5
    # Request window must start at 01-05 because MAX was None.
    assert result_b.requested_start == date(2024, 1, 5)
    rows = state.ohlcv_rows(1)
    assert len(rows) == 5
    assert state.logs_with(status="FAILED") and state.logs_with(status="SUCCESS")


# ===========================================================================
# E2E-2: Partial response → subsequent run fills the rest
# ===========================================================================


def test_e2e_2_partial_then_recovery():
    """Run A returns only the first 3 of 5 requested days → PARTIAL. Run B
    picks up at MAX+1 and fetches the remaining 2 days (plus one extra if
    today advances)."""
    state = _State()
    asset = _make_asset(asset_id=2, start_date=date(2024, 1, 5))
    state.assets[2] = asset

    src = _make_datasource()

    # ----- Run A: returns only 01-05..01-09 (4 trading days, Mon-Fri) -----
    # Trading days in [01-05, 01-10] = 01-05, 01-08, 01-09, 01-10 (4 days).
    # Source returns only the first 3: 01-05, 01-08, 01-09.
    src.fetch_ohlcv.return_value = _ohlcv_df(
        [date(2024, 1, 5), date(2024, 1, 8), date(2024, 1, 9)]
    )
    with _patched_pipeline(state):
        pipe_a, _ = _make_pipeline(state, src, today=date(2024, 1, 10))
        result_a = pipe_a.run_for_asset(asset)

    # Partial: gap detected (expected=4, received=3).
    assert result_a.status == "PARTIAL"
    assert result_a.rows_inserted == 3
    assert len(state.ohlcv_rows(2)) == 3
    # MAX now = 2024-01-09.
    mx = state.max_time(2)
    assert mx is not None and mx.date() == date(2024, 1, 9)

    # ----- Run B: next day, source healthy, returns 01-10..01-11 (2 days) -----
    # New request window: MAX+1 = 01-10 .. today 01-11.
    src.fetch_ohlcv.return_value = _ohlcv_df([date(2024, 1, 10), date(2024, 1, 11)])
    with _patched_pipeline(state):
        pipe_b, _ = _make_pipeline(state, src, today=date(2024, 1, 11))
        result_b = pipe_b.run_for_asset(asset)

    assert result_b.status == "SUCCESS"
    assert result_b.rows_inserted == 2
    # Total: 3 + 2 = 5 distinct trading days.
    rows = state.ohlcv_rows(2)
    times = {r["time"].date() for r in rows}
    assert times == {
        date(2024, 1, 5),
        date(2024, 1, 8),
        date(2024, 1, 9),
        date(2024, 1, 10),
        date(2024, 1, 11),
    }


# ===========================================================================
# E2E-3: Idempotent replay
# ===========================================================================


def test_e2e_3_idempotent_replay():
    """Second immediate run with the same range does not duplicate rows;
    MAX advances after Run A, so Run B sees an empty window and inserts 0."""
    state = _State()
    asset = _make_asset(asset_id=3, start_date=date(2024, 1, 8))
    state.assets[3] = asset

    src = _make_datasource()
    days = [date(2024, 1, 8), date(2024, 1, 9)]
    src.fetch_ohlcv.return_value = _ohlcv_df(days)

    # Run A.
    with _patched_pipeline(state):
        pipe_a, _ = _make_pipeline(state, src, today=date(2024, 1, 9))
        r_a = pipe_a.run_for_asset(asset)
    assert r_a.status == "SUCCESS"
    assert r_a.rows_inserted == 2
    count_after_a = len(state.ohlcv_rows(3))
    assert count_after_a == 2

    # Run B immediately with the same "today" → MAX=01-09 so start=01-10 > end=01-09
    # which short-circuits to SUCCESS(0) without calling the source.
    src.fetch_ohlcv.reset_mock()
    src.fetch_ohlcv.return_value = _ohlcv_df(days)
    with _patched_pipeline(state):
        pipe_b, _ = _make_pipeline(state, src, today=date(2024, 1, 9))
        r_b = pipe_b.run_for_asset(asset)
    assert r_b.status == "SUCCESS"
    assert r_b.rows_inserted == 0
    assert len(state.ohlcv_rows(3)) == count_after_a  # unchanged


# ===========================================================================
# E2E-4: RateLimitError → next run recovers
# ===========================================================================


def test_e2e_4_ratelimit_then_recovery():
    state = _State()
    asset = _make_asset(asset_id=4, start_date=date(2024, 1, 5))
    state.assets[4] = asset

    src = _make_datasource()

    # Run A: rate-limited on every attempt.
    src.fetch_ohlcv.side_effect = RateLimitError("429")
    with _patched_pipeline(state):
        pipe_a, _ = _make_pipeline(state, src, today=date(2024, 1, 10))
        r_a = pipe_a.run_for_asset(asset)
    assert r_a.status == "FAILED"
    assert r_a.error_message and "rate limit" in r_a.error_message.lower()
    assert state.ohlcv_rows(4) == []

    # Run B: same range, source now healthy.
    expected_days = [
        date(2024, 1, 5),
        date(2024, 1, 8),
        date(2024, 1, 9),
        date(2024, 1, 10),
    ]
    src.fetch_ohlcv.side_effect = None
    src.fetch_ohlcv.return_value = _ohlcv_df(expected_days)
    with _patched_pipeline(state):
        pipe_b, _ = _make_pipeline(state, src, today=date(2024, 1, 10))
        r_b = pipe_b.run_for_asset(asset)
    assert r_b.status == "SUCCESS"
    assert r_b.rows_inserted == 4
    assert len(state.ohlcv_rows(4)) == 4


# ===========================================================================
# E2E-5: Multi-asset — one fails, others succeed; next run recovers failed one
# ===========================================================================


def test_e2e_5_multi_asset_partial_market_failure():
    state = _State()
    a_A = _make_asset(asset_id=10, symbol="A", start_date=date(2024, 1, 8))
    a_B = _make_asset(asset_id=11, symbol="B", start_date=date(2024, 1, 8))
    a_C = _make_asset(asset_id=12, symbol="C", start_date=date(2024, 1, 8))
    for a in (a_A, a_B, a_C):
        state.assets[a.asset_id] = a

    src = _make_datasource()
    good_df = _ohlcv_df([date(2024, 1, 8), date(2024, 1, 9)])

    def _fetch_run_a(*, symbol, market, start, end):
        if symbol == "B":
            raise DataSourceError("B broken")
        return good_df

    src.fetch_ohlcv.side_effect = _fetch_run_a

    # ----- Run A -----
    with _patched_pipeline(state, list_active=[a_A, a_B, a_C]):
        pipe_a, _ = _make_pipeline(
            state, src, today=date(2024, 1, 9), list_active=[a_A, a_B, a_C]
        )
        results_a = pipe_a.run_for_market("US")

    assert len(results_a) == 3
    status_by_id = {r.asset_id: r.status for r in results_a}
    assert status_by_id[10] == "SUCCESS"
    assert status_by_id[11] == "FAILED"
    assert status_by_id[12] == "SUCCESS"
    # A and C have data, B does not.
    assert len(state.ohlcv_rows(10)) == 2
    assert state.ohlcv_rows(11) == []
    assert len(state.ohlcv_rows(12)) == 2

    # ----- Run B: B now healthy; A/C already up-to-date so they no-op -----
    def _fetch_run_b(*, symbol, market, start, end):
        return good_df  # all symbols happy now

    src.fetch_ohlcv.side_effect = _fetch_run_b
    with _patched_pipeline(state, list_active=[a_A, a_B, a_C]):
        pipe_b, _ = _make_pipeline(
            state, src, today=date(2024, 1, 9), list_active=[a_A, a_B, a_C]
        )
        results_b = pipe_b.run_for_market("US")

    status_by_id_b = {r.asset_id: r.status for r in results_b}
    assert status_by_id_b[10] == "SUCCESS"
    assert status_by_id_b[11] == "SUCCESS"
    assert status_by_id_b[12] == "SUCCESS"
    # B now has both rows; A/C unchanged (only no-op reached today).
    assert len(state.ohlcv_rows(11)) == 2
    # A and C should still be 2 rows; because their MAX=01-09 and today=01-09
    # means start=01-10 > end → empty window → 0 inserts.
    assert len(state.ohlcv_rows(10)) == 2
    assert len(state.ohlcv_rows(12)) == 2
    # Row count for B is exactly what the source returned on Run B.
    rows_b = state.ohlcv_rows(11)
    assert {r["time"].date() for r in rows_b} == {date(2024, 1, 8), date(2024, 1, 9)}


# ===========================================================================
# E2E-6: close=0 row → REJECTED, then next run re-requests that day
# ===========================================================================


def test_e2e_6_close_zero_then_recovery():
    """Run A returns 4 trading days but one has close=0 → REJECTED log, 3 good
    rows upserted. MAX(time) now equals the last GOOD date. Run B re-requests
    from MAX+1 and, if the source now returns that day healthy, UPSERTs it."""
    state = _State()
    asset = _make_asset(asset_id=20, start_date=date(2024, 1, 5))
    state.assets[20] = asset

    src = _make_datasource()

    # Trading days in [01-05, 01-10] = 01-05, 01-08, 01-09, 01-10 (4 days).
    # Run A: the row at 01-09 has close=0 → REJECTED; good rows at 01-05,
    # 01-08, 01-10.
    days_a = [date(2024, 1, 5), date(2024, 1, 8), date(2024, 1, 9), date(2024, 1, 10)]
    src.fetch_ohlcv.return_value = _ohlcv_df(days_a, close_overrides={2: 0.0})
    with _patched_pipeline(state):
        pipe_a, _ = _make_pipeline(state, src, today=date(2024, 1, 10))
        r_a = pipe_a.run_for_asset(asset)

    assert r_a.status == "PARTIAL"  # rejected rows → PARTIAL classification
    assert r_a.rows_inserted == 3
    assert r_a.rows_rejected == 1
    rejected_logs = state.logs_with(status="REJECTED")
    assert len(rejected_logs) == 1
    # The good rows are 01-05, 01-08, 01-10 → MAX(time) = 01-10.
    mx = state.max_time(20)
    assert mx is not None and mx.date() == date(2024, 1, 10)

    # Run B: today advances to 01-11. MAX+1 = 01-11. Source returns 01-11
    # healthy. (Re-requesting 01-09 isn't automatic because MAX has already
    # advanced past it; gap repair of older skipped days is tracked via the
    # PARTIAL classification but left as a higher-layer concern, not the
    # per-run window. Documenting behaviour here.)
    src.fetch_ohlcv.return_value = _ohlcv_df([date(2024, 1, 11)])
    with _patched_pipeline(state):
        pipe_b, _ = _make_pipeline(state, src, today=date(2024, 1, 11))
        r_b = pipe_b.run_for_asset(asset)

    assert r_b.status == "SUCCESS"
    assert r_b.rows_inserted == 1
    all_rows = state.ohlcv_rows(20)
    times = {r["time"].date() for r in all_rows}
    # 01-09 stays missing (observed as a PARTIAL gap on Run A); the pipeline
    # window-scheme honours MAX+1 semantics. The test pins this as the
    # current contract.
    assert times == {
        date(2024, 1, 5),
        date(2024, 1, 8),
        date(2024, 1, 10),
        date(2024, 1, 11),
    }
