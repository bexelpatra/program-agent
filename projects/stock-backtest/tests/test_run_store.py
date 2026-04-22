"""Unit tests for run_hash / run_store (TASK-018).

The target DB is Postgres + TimescaleDB which is unavailable in unit tests,
so every test below either:

1. exercises pure functions (hash helpers), or
2. mocks the SQLAlchemy ``Session`` so the repository layer's SQL is never
   actually executed.
"""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from stock_backtest.backtest import run_store
from stock_backtest.backtest.cache import (
    compute_code_commit_hash,
    compute_data_hash,
    compute_run_hash,
    is_stale,
)


# ---------------------------------------------------------------------------
# compute_run_hash
# ---------------------------------------------------------------------------
def test_compute_run_hash_deterministic() -> None:
    h1 = compute_run_hash(
        "fixed_weight",
        {"weights": {"SPY": 0.6, "AGG": 0.4}},
        ["SPY", "AGG"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Reordered universe and params dict must hash identically.
    h2 = compute_run_hash(
        "fixed_weight",
        {"weights": {"AGG": 0.4, "SPY": 0.6}},
        ["AGG", "SPY"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    assert h1 == h2
    assert re.fullmatch(r"[0-9a-f]{64}", h1)


def test_compute_run_hash_changes_on_input_change() -> None:
    base = compute_run_hash(
        "fw",
        {"w": 0.5},
        ["SPY"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Different strategy.
    assert base != compute_run_hash(
        "other",
        {"w": 0.5},
        ["SPY"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Different params.
    assert base != compute_run_hash(
        "fw",
        {"w": 0.6},
        ["SPY"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Different universe.
    assert base != compute_run_hash(
        "fw",
        {"w": 0.5},
        ["SPY", "AGG"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Different period.
    assert base != compute_run_hash(
        "fw",
        {"w": 0.5},
        ["SPY"],
        (_dt.date(2020, 1, 2), _dt.date(2024, 12, 31)),
        "USD",
    )
    # Different base ccy.
    assert base != compute_run_hash(
        "fw",
        {"w": 0.5},
        ["SPY"],
        (_dt.date(2020, 1, 1), _dt.date(2024, 12, 31)),
        "KRW",
    )


# ---------------------------------------------------------------------------
# compute_code_commit_hash
# ---------------------------------------------------------------------------
def test_compute_code_commit_hash_in_repo() -> None:
    h = compute_code_commit_hash()
    # Should be either 40-char hex (git installed & repo) or "unknown".
    assert h == "unknown" or re.fullmatch(r"[0-9a-f]{40}", h)


def test_compute_code_commit_hash_git_missing() -> None:
    with patch("subprocess.run", side_effect=FileNotFoundError()):
        assert compute_code_commit_hash() == "unknown"


def test_compute_code_commit_hash_nonzero_returncode() -> None:
    fake = SimpleNamespace(returncode=128, stdout="", stderr="fatal")
    with patch("subprocess.run", return_value=fake):
        assert compute_code_commit_hash() == "unknown"


# ---------------------------------------------------------------------------
# compute_data_hash
# ---------------------------------------------------------------------------
def _mock_session_with_rows(rows: list[tuple]) -> MagicMock:
    """Session whose ``execute`` returns an iterable of tuples."""
    session = MagicMock()
    session.execute.return_value = iter(rows)
    return session


def test_compute_data_hash_changes_with_max_time() -> None:
    t1 = _dt.datetime(2024, 6, 1, 0, 0, 0)
    t2 = _dt.datetime(2024, 6, 2, 0, 0, 0)

    s1 = _mock_session_with_rows([(1, t1, 100), (2, t1, 100)])
    s2 = _mock_session_with_rows([(1, t2, 100), (2, t1, 100)])

    h1 = compute_data_hash(s1, [1, 2])
    h2 = compute_data_hash(s2, [1, 2])
    assert h1 != h2


def test_compute_data_hash_changes_with_count() -> None:
    t = _dt.datetime(2024, 6, 1, 0, 0, 0)

    s1 = _mock_session_with_rows([(1, t, 100)])
    s2 = _mock_session_with_rows([(1, t, 101)])

    assert compute_data_hash(s1, [1]) != compute_data_hash(s2, [1])


def test_compute_data_hash_stable_on_reorder() -> None:
    t = _dt.datetime(2024, 6, 1, 0, 0, 0)
    s1 = _mock_session_with_rows([(1, t, 10), (2, t, 20)])
    s2 = _mock_session_with_rows([(2, t, 20), (1, t, 10)])
    # Both normalised by sorting asset_ids; input order shouldn't matter.
    assert compute_data_hash(s1, [1, 2]) == compute_data_hash(s2, [2, 1])


def test_compute_data_hash_empty_universe() -> None:
    session = MagicMock()
    # Should not hit the DB when no assets given.
    h = compute_data_hash(session, [])
    session.execute.assert_not_called()
    assert re.fullmatch(r"[0-9a-f]{64}", h)


# ---------------------------------------------------------------------------
# is_stale
# ---------------------------------------------------------------------------
def test_is_stale_true_when_hash_differs() -> None:
    t = _dt.datetime(2024, 6, 1, 0, 0, 0)
    session = _mock_session_with_rows([(1, t, 100)])
    run_row = SimpleNamespace(data_hash="deadbeef", universe=[1])
    assert is_stale(run_row, session) is True


def test_is_stale_false_when_hash_matches() -> None:
    t = _dt.datetime(2024, 6, 1, 0, 0, 0)
    # Prepare two independent "sessions" that produce the same rows so that
    # the live hash matches the stored one we pre-compute.
    pre_session = _mock_session_with_rows([(1, t, 100)])
    stored = compute_data_hash(pre_session, [1])

    live_session = _mock_session_with_rows([(1, t, 100)])
    run_row = SimpleNamespace(data_hash=stored, universe=[1])
    assert is_stale(run_row, live_session) is False


def test_is_stale_true_when_stored_none() -> None:
    session = MagicMock()
    run_row = SimpleNamespace(data_hash=None, universe=[1])
    assert is_stale(run_row, session) is True


def test_is_stale_accepts_universe_dicts() -> None:
    t = _dt.datetime(2024, 6, 1, 0, 0, 0)
    pre_session = _mock_session_with_rows([(1, t, 100), (2, t, 50)])
    stored = compute_data_hash(pre_session, [1, 2])

    live_session = _mock_session_with_rows([(1, t, 100), (2, t, 50)])
    run_row = SimpleNamespace(
        data_hash=stored,
        universe=[{"asset_id": 1, "symbol": "X"}, {"asset_id": 2, "symbol": "Y"}],
    )
    assert is_stale(run_row, live_session) is False


# ---------------------------------------------------------------------------
# save_run / find_cached_run
# ---------------------------------------------------------------------------


@dataclass
class _FakeSpec:
    asset_id: int
    symbol: str
    market: str = "US"
    currency: str = "USD"
    asset_class: str = "ETF"
    start_date: _dt.date | None = None
    end_date: _dt.date | None = None


@dataclass
class _FakeConfig:
    strategy_name: str
    params: dict
    universe: list
    period_start: _dt.date
    period_end: _dt.date
    base_currency: str = "USD"
    market_mode: str = "STOCK"


@dataclass
class _FakeTrade:
    date: _dt.date
    asset_id: int
    side: str
    qty: Decimal
    price: Decimal
    currency: str
    commission_bps: Decimal
    slippage_bps: Decimal


@dataclass
class _FakeResult:
    equity_curve: pd.Series
    trades: list
    run_hash: str | None = None


def _fake_result() -> _FakeResult:
    idx = pd.DatetimeIndex(
        [
            pd.Timestamp("2024-01-02"),
            pd.Timestamp("2024-01-03"),
            pd.Timestamp("2024-01-04"),
        ]
    )
    equity = pd.Series([100_000.0, 100_500.0, 99_800.0], index=idx, name="equity")
    trades = [
        _FakeTrade(
            date=_dt.date(2024, 1, 2),
            asset_id=1,
            side="BUY",
            qty=Decimal("10"),
            price=Decimal("400"),
            currency="USD",
            commission_bps=Decimal("15"),
            slippage_bps=Decimal("5"),
        )
    ]
    return _FakeResult(equity_curve=equity, trades=trades, run_hash="hash-abc")


def test_save_run_calls_all_repository_inserts() -> None:
    cfg = _FakeConfig(
        strategy_name="fw",
        params={"w": 0.5},
        universe=[_FakeSpec(asset_id=1, symbol="SPY")],
        period_start=_dt.date(2024, 1, 1),
        period_end=_dt.date(2024, 12, 31),
    )
    result = _fake_result()
    session = MagicMock()

    with patch.object(
        run_store, "insert_run", return_value=42
    ) as m_insert_run, patch.object(
        run_store, "bulk_insert_equity", return_value=3
    ) as m_eq, patch.object(
        run_store, "bulk_insert_trades", return_value=1
    ) as m_tr, patch.object(
        run_store, "insert_metrics", return_value=8
    ) as m_me:
        run_id = run_store.save_run(
            session=session,
            config=cfg,
            result=result,
            strategy_name="fw",
            data_hash="d-hash",
            code_hash="c-hash",
        )

    assert run_id == 42
    m_insert_run.assert_called_once()
    m_eq.assert_called_once()
    m_tr.assert_called_once()
    m_me.assert_called_once()

    # Inspect the kwargs to insert_run for correctness.
    _, kw = m_insert_run.call_args
    assert kw["run_hash"] == "hash-abc"
    assert kw["strategy_name"] == "fw"
    assert kw["code_commit_hash"] == "c-hash"
    assert kw["data_hash"] == "d-hash"
    assert kw["period_start"] == _dt.date(2024, 1, 1)
    assert kw["base_currency"] == "USD"
    assert kw["market_mode"] == "STOCK"
    assert kw["universe"] == [
        {"asset_id": 1, "symbol": "SPY", "market": "US", "currency": "USD"}
    ]

    # Equity rows shape: 3 points, drawdown monotone-non-positive.
    eq_args = m_eq.call_args.args
    assert eq_args[0] is session
    assert eq_args[1] == 42
    eq_rows = eq_args[2]
    assert len(eq_rows) == 3
    assert all("time" in r and "equity" in r and "drawdown" in r for r in eq_rows)

    # Trade rows shape.
    tr_args = m_tr.call_args.args
    assert tr_args[1] == 42
    assert tr_args[2][0]["asset_id"] == 1
    assert tr_args[2][0]["side"] == "BUY"
    assert pytest.approx(tr_args[2][0]["qty"]) == 10.0
    assert pytest.approx(tr_args[2][0]["price"]) == 400.0


def test_find_cached_run_returns_row_when_hash_matches() -> None:
    sentinel_row = SimpleNamespace(run_id=7, run_hash="h", data_hash="d")
    session = MagicMock()
    with patch.object(run_store, "get_run_by_hash", return_value=sentinel_row) as m_get:
        out = run_store.find_cached_run(session, "h")
    m_get.assert_called_once_with(session, "h")
    assert out is sentinel_row


def test_find_cached_run_returns_none_when_absent() -> None:
    session = MagicMock()
    with patch.object(run_store, "get_run_by_hash", return_value=None):
        assert run_store.find_cached_run(session, "missing") is None
