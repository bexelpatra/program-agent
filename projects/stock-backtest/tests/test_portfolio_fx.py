"""Regression tests for ``Portfolio._ensure_cash`` FX-spread monotonicity
(TASK-037).

These tests pin the architecture-decision-#4 invariant: in a cross-currency
rebalance, widening ``fx_spread_bps`` must produce a strictly **lower** final
equity than a narrower spread. Prior to TASK-037 the back-out inside
``_ensure_cash`` used ``FXConverter.convert`` with ``apply_spread=True`` in the
reverse direction, which made wider spreads *reduce* the source-currency
requirement and thereby *increase* final equity — the opposite of reality.

All tests are in-memory.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal

import numpy as np
import pandas as pd
import pytest

from stock_backtest.backtest.calendar import get_trading_days
from stock_backtest.backtest.engine import (
    AssetSpec,
    BacktestConfig,
    BacktestEngine,
)
from stock_backtest.backtest.fx import FXConverter
from stock_backtest.backtest.portfolio import Portfolio
from stock_backtest.config import Settings
from stock_backtest.strategies.base import Strategy, StrategyParams


# ---------------------------------------------------------------------------
# Helpers (mirrors test_engine_regression.py shape; intentionally duplicated
# to keep this file self-contained — we are not allowed to edit that file.)
# ---------------------------------------------------------------------------


class _DummyParams(StrategyParams):
    pass


class _SingleAssetStrategy(Strategy):
    name = "single_asset_fxtest"
    params_schema = _DummyParams
    description = "100% first asset."

    def generate_weights(self, prices, rebalance_dates):
        cols = list(prices.columns)
        data = {cols[0]: [1.0] * len(rebalance_dates)}
        for c in cols[1:]:
            data[c] = [0.0] * len(rebalance_dates)
        return pd.DataFrame(data, index=rebalance_dates)

    def required_universe(self):
        return None


def _settings(spread_bps: int) -> Settings:
    return Settings.model_validate(
        {
            "base_currency": "USD",
            "market_mode": "STOCK",
            "costs": {
                "commission_buy_bps": 5,
                "commission_sell_bps": 5,
                "slippage_bps": 3,
                "fx_spread_bps": spread_bps,
                "market_overrides": {},
            },
            "rebalance": {"frequency": "Y"},
            "calendars": {"US": "XNYS"},
            "tax": {
                "enabled": False,
                "profile": "none",
                "profiles": {"none": {}},
            },
        }
    )


def _fx(sessions: pd.DatetimeIndex, spread_bps: int) -> FXConverter:
    pairs = {("USD", "EUR"): 0.9, ("EUR", "KRW"): 1500.0, ("USD", "KRW"): 1350.0}
    overrides: dict = {}
    for ts in sessions:
        d = ts.date()
        for (b, q), rate in pairs.items():
            overrides[(b, q, d)] = Decimal(str(rate))
            overrides[(q, b, d)] = Decimal(1) / Decimal(str(rate))
    return FXConverter(session=None, fx_spread_bps=spread_bps, rate_overrides=overrides)


def _loader(sessions, values):
    def _inner(universe, start, end):
        data = {aid: pd.Series(v, index=sessions) for aid, v in values.items()}
        return pd.DataFrame(data)

    return _inner


def _run(spread_bps: int) -> float:
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 6, 30)
    sessions = get_trading_days("US", start, end)
    n = len(sessions)
    prices = {1: [100.0] * n}

    asset = AssetSpec(1, "BMW.DE", "US", "EUR", "overseas_etf", start, end)
    config = BacktestConfig(
        strategy_name="single_asset_fxtest",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="Y",
    )
    engine = BacktestEngine(
        _settings(spread_bps),
        session_factory=None,
        price_loader=_loader(sessions, prices),
        fx_converter=_fx(sessions, spread_bps),
    )
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))
    return float(result.equity_curve.iloc[-1])


# ---------------------------------------------------------------------------
# Monotonicity: wider spread -> lower final equity.
# ---------------------------------------------------------------------------


def test_fx_spread_monotonic_decrease_in_equity():
    """EUR-denominated asset bought from a USD cash bucket: final equity must
    decrease strictly as ``fx_spread_bps`` widens.
    """
    eq_0 = _run(0)
    eq_100 = _run(100)
    eq_300 = _run(300)

    assert (
        eq_100 < eq_0
    ), f"100bps spread did not reduce equity: 0bps={eq_0}, 100bps={eq_100}"
    assert (
        eq_300 < eq_100
    ), f"300bps not worse than 100bps: 100bps={eq_100}, 300bps={eq_300}"
    # Sanity bound: the base run with zero spread should still be close to 100k.
    assert 99_000 < eq_0 < 101_000, f"base run equity unexpected: {eq_0}"


# ---------------------------------------------------------------------------
# Unit test for _ensure_cash directly.
# ---------------------------------------------------------------------------


def test_ensure_cash_consumes_more_source_at_wider_spread():
    """Directly exercise ``Portfolio._ensure_cash``: going from 1bps to
    300bps spread, the USD drained to acquire the same EUR amount must
    strictly increase.
    """
    date = _dt.date(2022, 6, 15)
    pairs = {("USD", "EUR", date): Decimal("0.9")}

    def _drain(spread_bps: int) -> Decimal:
        fx = FXConverter(session=None, fx_spread_bps=spread_bps, rate_overrides=pairs)
        p = Portfolio.from_initial(
            "USD", {"USD": Decimal("10000"), "EUR": Decimal("0")}
        )
        p._ensure_cash("EUR", Decimal("900"), fx, date)
        # USD spent = 10000 - remaining USD.
        return Decimal("10000") - p.cash_by_ccy["USD"]

    spent_low = _drain(1)
    spent_mid = _drain(100)
    spent_high = _drain(300)
    assert spent_low < spent_mid < spent_high, (
        f"source drain not monotonic in spread: low={spent_low}, "
        f"mid={spent_mid}, high={spent_high}"
    )
    # Mid rate 0.9 USD->EUR => 900 EUR needs 1000 USD at mid.
    # With 0 spread we should spend ~1000 USD.
    assert abs(spent_low - Decimal("1000")) < Decimal("1")
