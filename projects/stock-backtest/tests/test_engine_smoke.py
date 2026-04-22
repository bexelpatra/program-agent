"""Smoke tests for the vectorised backtest engine.

These tests bypass the database entirely by injecting a hand-crafted price
loader and an in-memory :class:`FXConverter`. They exist to verify that the
engine composes correctly end-to-end with / without tax enabled.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal

import numpy as np
import pandas as pd
import pytest

from stock_backtest.backtest.engine import (
    AssetSpec,
    BacktestConfig,
    BacktestEngine,
)
from stock_backtest.backtest.fx import FXConverter
from stock_backtest.config import Settings
from stock_backtest.strategies.base import Strategy, StrategyParams


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _DummyParams(StrategyParams):
    pass


class _SingleAssetStrategy(Strategy):
    """100% allocation to the first universe symbol, rebalanced every period."""

    name = "single_asset_fixed"
    params_schema = _DummyParams
    description = "Test helper: always 100% first asset."

    def generate_weights(self, prices, rebalance_dates):
        if len(prices.columns) == 0 or len(rebalance_dates) == 0:
            return pd.DataFrame(index=rebalance_dates)
        first = prices.columns[0]
        data = {first: [1.0] * len(rebalance_dates)}
        for other in prices.columns[1:]:
            data[other] = [0.0] * len(rebalance_dates)
        return pd.DataFrame(data, index=rebalance_dates)

    def required_universe(self):
        return None


def _make_price_loader(
    sessions: pd.DatetimeIndex, asset_ids: list[int], start_price: float = 100.0
):
    """Return a PriceLoader that fabricates a smooth rising price series."""

    def _loader(universe, start, end):
        data = {}
        for i, aid in enumerate(asset_ids):
            # Mild drift + deterministic noise so the series is monotone-ish but not flat.
            n = len(sessions)
            series = start_price * (
                1.0 + 0.0003 * np.arange(n) + 0.001 * ((i + 1) * 0.5)
            )
            data[aid] = pd.Series(series, index=sessions)
        return pd.DataFrame(data)

    return _loader


def _default_settings(tax_enabled: bool) -> Settings:
    base = {
        "base_currency": "USD",
        "market_mode": "STOCK",
        "costs": {
            "commission_buy_bps": 5,
            "commission_sell_bps": 5,
            "slippage_bps": 3,
            "fx_spread_bps": 20,
            "market_overrides": {},
        },
        "rebalance": {"frequency": "ME"},
        "calendars": {"US": "XNYS"},
        "tax": {
            "enabled": tax_enabled,
            "profile": "kr_resident" if tax_enabled else "none",
            "profiles": {
                "kr_resident": {
                    "overseas_capital_gains_rate": 0.22,
                    "overseas_annual_deduction_krw": 2_500_000,
                    "overseas_dividend_rate": 0.154,
                    "crypto_enabled": True,
                    "crypto_capital_gains_rate": 0.22,
                    "crypto_annual_deduction_krw": 2_500_000,
                },
                "none": {},
            },
        },
    }
    return Settings.model_validate(base)


def _build_fx(dates: pd.DatetimeIndex) -> FXConverter:
    overrides = {}
    for ts in dates:
        d = ts.date()
        overrides[("USD", "KRW", d)] = Decimal("1350")
        overrides[("KRW", "USD", d)] = Decimal("1") / Decimal("1350")
    return FXConverter(session=None, fx_spread_bps=20, rate_overrides=overrides)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def _run_once(tax_enabled: bool):
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2023, 12, 29)

    from stock_backtest.backtest.calendar import get_trading_days

    sessions = get_trading_days("US", start, end)
    asset = AssetSpec(
        asset_id=1,
        symbol="SPY",
        market="US",
        currency="USD",
        asset_class="overseas_etf",
        start_date=start,
        end_date=end,
    )
    config = BacktestConfig(
        strategy_name="single_asset_fixed",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )

    settings = _default_settings(tax_enabled=tax_enabled)
    price_loader = _make_price_loader(sessions, [1])
    fx = _build_fx(sessions)
    engine = BacktestEngine(
        settings,
        session_factory=None,
        price_loader=price_loader,
        fx_converter=fx,
    )
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))
    return result


def test_smoke_no_tax():
    result = _run_once(tax_enabled=False)
    assert len(result.equity_curve) > 0
    assert float(result.equity_curve.iloc[0]) == pytest.approx(100_000.0, rel=1e-2)
    assert float(result.equity_curve.iloc[-1]) > 0
    # No tax path should not record tax debits.
    for year, tax in result.tax_paid_by_year.items():
        assert tax == Decimal("0")
    assert result.run_hash is not None and len(result.run_hash) == 64


def test_smoke_with_tax():
    result = _run_once(tax_enabled=True)
    assert len(result.equity_curve) > 0
    assert float(result.equity_curve.iloc[0]) == pytest.approx(100_000.0, rel=1e-2)
    assert float(result.equity_curve.iloc[-1]) > 0
    # Multiple rebalances should have produced at least a handful of trades.
    assert len(result.trades) > 0
