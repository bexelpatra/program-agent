"""Unit + regression tests for the dynamic rebalance cushion (TASK-038).

Previously ``_build_rebalance_trades`` reserved a hard-coded 50bps cushion
(``equity * 0.995``). With ``fx_spread_bps > 50`` the first BUY would
overdraft cash and ``_ensure_cash`` raised ``InsufficientFundsError``.

These tests pin the new behaviour:

1. High ``fx_spread_bps`` (100bps) is handled without error.
2. Larger cost configs produce larger cushions (the cushion scales with
   ``commission_buy_bps + slippage_bps + fx_spread_bps``).
3. Single-currency universes do not pay an fx-spread cushion component.
4. The cushion is capped at 500bps (5%) even under pathological configs.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal

import numpy as np
import pytest

from stock_backtest.backtest.engine import (
    AssetSpec,
    BacktestConfig,
    BacktestEngine,
)

from tests.test_engine_regression import (
    _DummyParams,
    _SingleAssetStrategy,
    _build_fx,
    _const_loader,
    _default_settings,
    _us_sessions,
)


# ---------------------------------------------------------------------------
# 1. fx_spread_bps=100: previously InsufficientFundsError, now succeeds.
# ---------------------------------------------------------------------------


def test_large_fx_spread_does_not_raise_insufficient_funds():
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 6, 30)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    prices = {1: [100.0] * n}
    asset = AssetSpec(1, "BMW.DE", "US", "EUR", "overseas_etf", start, end)
    config = BacktestConfig(
        strategy_name="single_asset",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="Y",
    )

    settings = _default_settings(tax_enabled=False, fx_spread_bps=100)
    pairs = {("USD", "EUR"): 0.9, ("EUR", "KRW"): 1500.0, ("USD", "KRW"): 1350.0}
    fx = _build_fx(sessions, pairs=pairs, fx_spread_bps=100)
    loader = _const_loader(sessions, prices)
    engine = BacktestEngine(
        settings, session_factory=None, price_loader=loader, fx_converter=fx
    )

    # Must complete without InsufficientFundsError.
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))
    assert len(result.equity_curve) == n
    buys = [t for t in result.trades if t.side == "BUY"]
    assert len(buys) == 1


# ---------------------------------------------------------------------------
# 2. Cushion scales with the sum of cost bps.
# ---------------------------------------------------------------------------


def test_cushion_scales_with_cost_bps():
    """Higher total cost bps -> larger cushion -> more cash left untraded."""
    settings_low = _default_settings(tax_enabled=False, fx_spread_bps=5)
    settings_high = _default_settings(tax_enabled=False, fx_spread_bps=100)

    engine_low = BacktestEngine(settings_low, session_factory=None)
    engine_high = BacktestEngine(settings_high, session_factory=None)

    # Need fx component to kick in: universe currency != base.
    low = engine_low._compute_cushion_bps(
        universe_currencies={"EUR"}, base_currency="USD", markets={"US"}
    )
    high = engine_high._compute_cushion_bps(
        universe_currencies={"EUR"}, base_currency="USD", markets={"US"}
    )
    assert high > low
    # Difference in fx_spread is 95bps; the cushion should reflect that.
    assert (high - low) == Decimal("95")


# ---------------------------------------------------------------------------
# 3. Single-currency universes omit the fx component.
# ---------------------------------------------------------------------------


def test_cushion_no_fx_spread_when_single_currency():
    """When every universe asset is already in base_currency, fx_spread is 0."""
    settings = _default_settings(tax_enabled=False, fx_spread_bps=200)
    engine = BacktestEngine(settings, session_factory=None)

    single = engine._compute_cushion_bps(
        universe_currencies={"USD"}, base_currency="USD", markets={"US"}
    )
    cross = engine._compute_cushion_bps(
        universe_currencies={"USD", "EUR"}, base_currency="USD", markets={"US"}
    )

    # single-currency: commission_buy(5) + slippage(3) + safety(10) = 18 bps.
    # cross: +200 for fx_spread.
    assert single == Decimal("18")
    assert cross == Decimal("218")


# ---------------------------------------------------------------------------
# 4. Cushion is clamped at 500bps and logs a warning.
# ---------------------------------------------------------------------------


def test_cushion_is_clamped_to_max(caplog):
    """Pathological config -> cushion still capped at 500bps (5%)."""
    settings = _default_settings(tax_enabled=False, fx_spread_bps=10_000)
    engine = BacktestEngine(settings, session_factory=None)

    with caplog.at_level("WARNING"):
        cushion = engine._compute_cushion_bps(
            universe_currencies={"USD", "EUR"},
            base_currency="USD",
            markets={"US"},
        )

    assert cushion == Decimal("500")
    assert any("cushion" in rec.message for rec in caplog.records)


# ---------------------------------------------------------------------------
# 5. Cushion picks the most conservative market override.
# ---------------------------------------------------------------------------


def test_cushion_uses_most_conservative_market_override():
    """When universe spans multiple markets, pick the largest cost per bucket."""
    # Build a settings object with a KR override larger than US defaults.
    base = {
        "base_currency": "USD",
        "market_mode": "STOCK",
        "costs": {
            "commission_buy_bps": 5,
            "commission_sell_bps": 5,
            "slippage_bps": 3,
            "fx_spread_bps": 20,
            "market_overrides": {
                "KR": {"commission_buy_bps": 30, "slippage_bps": 8},
                "US": {"commission_buy_bps": 5, "slippage_bps": 3},
            },
        },
        "rebalance": {"frequency": "ME"},
        "calendars": {"US": "XNYS", "KR": "XKRX"},
        "tax": {
            "enabled": False,
            "profile": "none",
            "profiles": {"none": {}},
        },
    }
    from stock_backtest.config import Settings

    settings = Settings.model_validate(base)
    engine = BacktestEngine(settings, session_factory=None)

    cushion = engine._compute_cushion_bps(
        universe_currencies={"USD", "KRW"},
        base_currency="USD",
        markets={"US", "KR"},
    )
    # max_commission_buy = 30 (KR), max_slippage = 8 (KR),
    # max_fx_spread = 20 (both inherit default), safety = 10.
    # Total: 30 + 8 + 20 + 10 = 68.
    assert cushion == Decimal("68")
