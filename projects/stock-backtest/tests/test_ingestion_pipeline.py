"""Unit/integration tests for :mod:`stock_backtest.ingestion.pipeline`.

Covers TASK-012:
    1) Normal incremental ingestion (MAX(time)+1 .. today).
    2) First backfill (MAX==None → asset.start_date).
    3) Retry with exponential backoff on transient errors.
    4) All three retries fail → FAILED, exception absorbed.
    5) RateLimitError classification/logging.
    6) close=0/NaN/None row REJECTED, valid rows upserted.
    7) Idempotency: same data twice → second call still UPSERTs (no duplicate
       insert semantic - just call_count assertions on mocks).
    8) Non-trading-day filtering (weekends excluded).
    9) Gap recovery: stale MAX(time) still advances on next run.
   10) ``run_for_market`` — one asset fails, others still succeed, list returned.

The tests stub the DataSource, session, and repository collaborators via
``unittest.mock`` so no network / DB is required.
"""

from __future__ import annotations

import math
from contextlib import contextmanager
from datetime import date, datetime, timezone
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from stock_backtest.ingestion.base import (
    DataSource,
    DataSourceError,
    RateLimitError,
    SymbolNotFoundError,
)
from stock_backtest.ingestion.pipeline import IngestionPipeline, IngestionResult


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _make_settings(
    retry_max: int = 3,
    backoffs: tuple[float, ...] = (1.0, 2.0, 4.0),
) -> Any:
    """Lightweight duck-typed Settings object for the pipeline."""
    return SimpleNamespace(
        ingestion=SimpleNamespace(
            retry_max=retry_max,
            retry_backoff_seconds=list(backoffs),
        )
    )


def _make_asset(
    *,
    asset_id: int = 1,
    symbol: str = "SPY",
    market: str = "US",
    start_date: date | None = date(2023, 1, 1),
    meta: dict | None = None,
) -> Any:
    """Duck-typed asset object matching :class:`Asset` attribute surface."""
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
    """Build a minimal OHLCV DataFrame for the given dates.

    ``close_overrides`` maps positional index → close value (to inject
    None/NaN/0 etc.).
    """
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
    """Minimal session stand-in. Records commit/rollback/close call counts."""

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


def _make_session_factory(session: _FakeSession) -> Any:
    """Return a callable that returns the *same* session on every call."""

    def factory() -> _FakeSession:
        return session

    return factory


def _make_datasource(source_name: str = "yfinance") -> MagicMock:
    src = MagicMock(spec=DataSource)
    # ``spec=DataSource`` treats ``source_name`` as a mocked attribute, not a
    # property; assigning works fine.
    src.source_name = source_name
    return src


# A patch target helper: patch the pipeline's imported repository classes so
# no DB is touched.
@contextmanager
def _patch_repos(
    *,
    max_time: datetime | None = None,
    list_active: list | None = None,
):
    """Patch OhlcvRepository / IngestionLogRepository / AssetRepository where
    the pipeline module imports them."""
    ohlcv_repo = MagicMock()
    ohlcv_repo.get_max_time.return_value = max_time
    ohlcv_repo.upsert_bulk.side_effect = lambda asset_id, rows: len(rows)

    log_repo = MagicMock()
    # log() returns something truthy (IngestionLog-ish)
    log_repo.log.return_value = MagicMock()

    asset_repo = MagicMock()
    asset_repo.list_active.return_value = list_active or []

    with patch(
        "stock_backtest.ingestion.pipeline.OhlcvRepository",
        return_value=ohlcv_repo,
    ), patch(
        "stock_backtest.ingestion.pipeline.IngestionLogRepository",
        return_value=log_repo,
    ), patch(
        "stock_backtest.ingestion.pipeline.AssetRepository",
        return_value=asset_repo,
    ):
        yield SimpleNamespace(ohlcv=ohlcv_repo, log=log_repo, asset=asset_repo)


# Fake trading-days helper we substitute for ``get_trading_days`` so the
# pipeline's calendar layer is fully deterministic.
def _weekday_trading_days(_market, start, end):
    """Business-day calendar (Mon-Fri) regardless of market."""
    idx = pd.date_range(start=start, end=end, freq="B")
    return pd.DatetimeIndex(idx).normalize()


# ---------------------------------------------------------------------------
# 1) Normal incremental ingestion
# ---------------------------------------------------------------------------


def test_incremental_from_max_time_plus_one():
    """MAX(time)+1 day through today is used as the requested range; SUCCESS
    log is written and last_ingested_at is updated."""
    asset = _make_asset(asset_id=7, symbol="SPY", market="US")
    today = date(2024, 1, 10)  # Wed

    # Previously have data up to Jan 5 (Fri).
    max_time = datetime(2024, 1, 5, tzinfo=timezone.utc)

    trading_days = [date(2024, 1, 8), date(2024, 1, 9), date(2024, 1, 10)]  # Mon..Wed
    df = _ohlcv_df(trading_days)

    src = _make_datasource()
    src.fetch_ohlcv.return_value = df

    session = _FakeSession()
    settings = _make_settings()
    sleeps: list[float] = []

    with _patch_repos(max_time=max_time) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(session),
            settings=settings,
            today_fn=lambda: today,
            sleep_fn=sleeps.append,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SUCCESS"
    assert result.rows_inserted == 3
    assert result.rows_rejected == 0
    # start of request window should be max_time+1 = 2024-01-06.
    assert result.requested_start == date(2024, 1, 6)
    assert result.requested_end == today

    # DataSource called once (no retries needed), with the incremental window.
    assert src.fetch_ohlcv.call_count == 1
    kwargs = src.fetch_ohlcv.call_args.kwargs
    assert kwargs["symbol"] == "SPY"
    assert kwargs["market"] == "US"
    assert kwargs["start"] == date(2024, 1, 6)
    assert kwargs["end"] == today

    # UPSERT called exactly once with 3 rows.
    repos.ohlcv.upsert_bulk.assert_called_once()
    args, _ = repos.ohlcv.upsert_bulk.call_args
    assert args[0] == 7
    assert len(args[1]) == 3

    # SUCCESS ingestion_log recorded.
    log_statuses = [call.kwargs.get("status") for call in repos.log.log.call_args_list]
    assert "SUCCESS" in log_statuses
    assert "REJECTED" not in log_statuses

    # last_ingested_at updated.
    repos.asset.update_last_ingested.assert_called_once()
    # Committed exactly once.
    assert session.committed == 1
    assert session.rolled_back == 0


# ---------------------------------------------------------------------------
# 2) First backfill — MAX(time) is None → use asset.start_date.
# ---------------------------------------------------------------------------


def test_first_backfill_uses_asset_start_date():
    asset = _make_asset(symbol="AAPL", market="US", start_date=date(2024, 1, 2))
    today = date(2024, 1, 5)  # Fri

    trading_days = [
        date(2024, 1, 2),
        date(2024, 1, 3),
        date(2024, 1, 4),
        date(2024, 1, 5),
    ]
    df = _ohlcv_df(trading_days)
    src = _make_datasource()
    src.fetch_ohlcv.return_value = df

    session = _FakeSession()
    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(session),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SUCCESS"
    assert result.requested_start == date(2024, 1, 2)
    assert result.requested_end == today
    kwargs = src.fetch_ohlcv.call_args.kwargs
    assert kwargs["start"] == date(2024, 1, 2)


# ---------------------------------------------------------------------------
# 3) Retry with exponential backoff — 2 transient failures, 3rd succeeds.
# ---------------------------------------------------------------------------


def test_retry_then_success_calls_sleep_with_backoff():
    asset = _make_asset(start_date=date(2024, 1, 8))
    today = date(2024, 1, 9)  # Tue
    trading_days = [date(2024, 1, 8), date(2024, 1, 9)]
    df = _ohlcv_df(trading_days)

    src = _make_datasource()
    src.fetch_ohlcv.side_effect = [
        DataSourceError("transient #1"),
        DataSourceError("transient #2"),
        df,
    ]

    sleeps: list[float] = []
    session = _FakeSession()
    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(session),
            settings=_make_settings(retry_max=3, backoffs=(1.0, 2.0, 4.0)),
            today_fn=lambda: today,
            sleep_fn=sleeps.append,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SUCCESS"
    assert src.fetch_ohlcv.call_count == 3
    # Two sleeps before the final (successful) attempt. The third backoff is
    # never consumed because attempt #3 succeeds.
    assert sleeps == [1.0, 2.0]


# ---------------------------------------------------------------------------
# 4) All three retries fail → FAILED, pipeline doesn't raise.
# ---------------------------------------------------------------------------


def test_three_failures_yield_failed_status_and_log():
    asset = _make_asset()
    today = date(2024, 1, 9)

    src = _make_datasource()
    src.fetch_ohlcv.side_effect = DataSourceError("boom")

    sleeps: list[float] = []
    session = _FakeSession()
    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(session),
            settings=_make_settings(retry_max=3, backoffs=(1.0, 2.0, 4.0)),
            today_fn=lambda: today,
            sleep_fn=sleeps.append,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "FAILED"
    assert result.error_message and "data source error" in result.error_message
    # Exactly retry_max attempts.
    assert src.fetch_ohlcv.call_count == 3
    # Between 3 attempts there are 2 sleeps (the last attempt has no follow-up
    # wait, since we abort immediately once we've exhausted retries).
    assert sleeps == [1.0, 2.0]

    # FAILED ingestion_log recorded.
    log_statuses = [call.kwargs.get("status") for call in repos.log.log.call_args_list]
    assert log_statuses.count("FAILED") >= 1

    # No upsert should have been attempted.
    repos.ohlcv.upsert_bulk.assert_not_called()


# ---------------------------------------------------------------------------
# 5) RateLimitError classification
# ---------------------------------------------------------------------------


def test_ratelimit_error_logged_with_rate_limit_message():
    asset = _make_asset()
    today = date(2024, 1, 9)

    src = _make_datasource()
    src.fetch_ohlcv.side_effect = RateLimitError("429 too many")

    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(retry_max=3, backoffs=(1.0, 2.0, 4.0)),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "FAILED"
    assert "rate limit" in (result.error_message or "").lower()
    # Still retried retry_max times.
    assert src.fetch_ohlcv.call_count == 3

    # The FAILED ingestion_log carries a rate-limit hint.
    failed_msgs = [
        call.kwargs.get("error_message")
        for call in repos.log.log.call_args_list
        if call.kwargs.get("status") == "FAILED"
    ]
    assert any("rate limit" in (m or "").lower() for m in failed_msgs)


# ---------------------------------------------------------------------------
# 6) Mixed valid / invalid rows — only valid rows UPSERTed; REJECTED log added.
# ---------------------------------------------------------------------------


def test_rejects_invalid_close_and_logs_rejected():
    asset = _make_asset()
    today = date(2024, 1, 12)  # Fri
    trading_days = [
        date(2024, 1, 8),
        date(2024, 1, 9),
        date(2024, 1, 10),
        date(2024, 1, 11),
        date(2024, 1, 12),
    ]
    # Bad rows at index 1 (None), 2 (NaN), 3 (zero). Indexes 0 and 4 are good.
    df = _ohlcv_df(
        trading_days,
        close_overrides={1: None, 2: float("nan"), 3: 0.0},
    )
    src = _make_datasource()
    src.fetch_ohlcv.return_value = df

    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    # 5 trading days, 3 rejected → PARTIAL (gap = 3, rejected = 3).
    assert result.status == "PARTIAL"
    assert result.rows_inserted == 2
    assert result.rows_rejected == 3

    # UPSERT called with only the 2 good rows.
    repos.ohlcv.upsert_bulk.assert_called_once()
    args, _ = repos.ohlcv.upsert_bulk.call_args
    assert len(args[1]) == 2
    # All upserted rows have a finite, non-zero close.
    for row in args[1]:
        c = row["close"]
        assert c is not None and c != 0 and not math.isnan(float(c))

    # Exactly one REJECTED log and one PARTIAL log.
    log_statuses = [call.kwargs.get("status") for call in repos.log.log.call_args_list]
    assert log_statuses.count("REJECTED") == 1
    assert log_statuses.count("PARTIAL") == 1


# ---------------------------------------------------------------------------
# 7) Idempotency — running twice yields two UPSERTs with same payload.
# ---------------------------------------------------------------------------


def test_idempotent_upsert_on_repeat_run():
    asset = _make_asset(start_date=date(2024, 1, 8))
    today = date(2024, 1, 9)
    trading_days = [date(2024, 1, 8), date(2024, 1, 9)]
    df = _ohlcv_df(trading_days)

    src = _make_datasource()
    src.fetch_ohlcv.return_value = df

    # Both runs see the *same* MAX(time)==None, which is the worst-case
    # idempotency test: the pipeline should still only UPSERT the same rows
    # without raising (UPSERT semantics in the repo).
    with _patch_repos(max_time=None) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        r1 = pipe.run_for_asset(asset)
        r2 = pipe.run_for_asset(asset)

    assert r1.status == r2.status == "SUCCESS"
    assert r1.rows_inserted == r2.rows_inserted == 2
    # Two upsert calls with identical payload length.
    assert repos.ohlcv.upsert_bulk.call_count == 2
    first_rows = repos.ohlcv.upsert_bulk.call_args_list[0].args[1]
    second_rows = repos.ohlcv.upsert_bulk.call_args_list[1].args[1]
    assert len(first_rows) == len(second_rows) == 2


# ---------------------------------------------------------------------------
# 8) Non-trading-day filtering — weekend range filtered out by calendar.
# ---------------------------------------------------------------------------


def test_weekend_only_range_skipped_without_datasource_call():
    """When the requested window contains only weekends, the pipeline must
    return SUCCESS(rows=0) without ever contacting the data source."""
    asset = _make_asset()
    # Sat + Sun only.
    today = date(2024, 1, 7)  # Sun
    max_time = datetime(2024, 1, 5, tzinfo=timezone.utc)  # Fri

    src = _make_datasource()
    with _patch_repos(max_time=max_time) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SUCCESS"
    assert result.rows_inserted == 0
    src.fetch_ohlcv.assert_not_called()
    repos.ohlcv.upsert_bulk.assert_not_called()


# ---------------------------------------------------------------------------
# 9) Gap recovery — a previous partial run left MAX(time) behind; next run
#    covers the missed dates.
# ---------------------------------------------------------------------------


def test_gap_recovery_uses_max_time_plus_one_on_next_run():
    asset = _make_asset()

    # Suppose previous run ingested only through Jan 3. MAX(time) = Jan 3.
    max_time = datetime(2024, 1, 3, tzinfo=timezone.utc)  # Wed
    today = date(2024, 1, 9)  # Tue of the next week
    # Expected request window: Jan 4 (Thu) .. Jan 9 (Tue), trading days:
    # Jan 4, 5, 8, 9 (4 weekdays, weekend skipped).
    expected_trading = [
        date(2024, 1, 4),
        date(2024, 1, 5),
        date(2024, 1, 8),
        date(2024, 1, 9),
    ]
    df = _ohlcv_df(expected_trading)

    src = _make_datasource()
    src.fetch_ohlcv.return_value = df

    with _patch_repos(max_time=max_time) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SUCCESS"
    assert result.rows_inserted == 4
    # Request window must START on Jan 4, not on the earlier gap.
    assert src.fetch_ohlcv.call_args.kwargs["start"] == date(2024, 1, 4)
    assert src.fetch_ohlcv.call_args.kwargs["end"] == today


# ---------------------------------------------------------------------------
# 10) run_for_market — one asset fails, others still succeed, full list returned.
# ---------------------------------------------------------------------------


def test_run_for_market_isolates_failures_per_asset():
    a1 = _make_asset(asset_id=1, symbol="SPY", start_date=date(2024, 1, 8))
    a2 = _make_asset(asset_id=2, symbol="QQQ", start_date=date(2024, 1, 8))
    a3 = _make_asset(asset_id=3, symbol="IWM", start_date=date(2024, 1, 8))
    today = date(2024, 1, 9)
    trading_days = [date(2024, 1, 8), date(2024, 1, 9)]
    good_df = _ohlcv_df(trading_days)

    src = _make_datasource()

    # a1 succeeds, a2 always fails (all retries), a3 succeeds.
    def _fetch(*, symbol, market, start, end):
        if symbol == "QQQ":
            raise DataSourceError("broken")
        return good_df

    src.fetch_ohlcv.side_effect = _fetch

    with _patch_repos(max_time=None, list_active=[a1, a2, a3]) as repos, patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        results = pipe.run_for_market("US")

    assert len(results) == 3
    status_by_id = {r.asset_id: r.status for r in results}
    assert status_by_id[1] == "SUCCESS"
    assert status_by_id[2] == "FAILED"
    assert status_by_id[3] == "SUCCESS"


# ---------------------------------------------------------------------------
# Additional: SymbolNotFound → SKIPPED, immediate (no retry).
# ---------------------------------------------------------------------------


def test_symbol_not_found_skipped_without_retry():
    asset = _make_asset()
    today = date(2024, 1, 9)

    src = _make_datasource()
    src.fetch_ohlcv.side_effect = SymbolNotFoundError("no such symbol")

    with _patch_repos(max_time=None), patch(
        "stock_backtest.ingestion.pipeline.get_trading_days",
        side_effect=_weekday_trading_days,
    ):
        pipe = IngestionPipeline(
            sources={"US": src},
            session_factory=_make_session_factory(_FakeSession()),
            settings=_make_settings(retry_max=3),
            today_fn=lambda: today,
            sleep_fn=lambda _s: None,
        )
        result = pipe.run_for_asset(asset)

    assert result.status == "SKIPPED"
    # SymbolNotFoundError is NOT retried.
    assert src.fetch_ohlcv.call_count == 1
