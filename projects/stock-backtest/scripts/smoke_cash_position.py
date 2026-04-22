"""Smoke script: verify the engine honours the reserved ``_CASH_`` symbol.

Given a strategy that returns ``{"SPY": 0.6, "_CASH_": 0.4}``, the engine
must:

- **never** emit BUY/SELL trades for ``_CASH_``
- invest roughly 60% of initial equity into SPY
- leave roughly 40% of initial equity idle in ``cash_by_ccy["USD"]``

See architecture.md section "전략 DSL 및 현금 1급 처리".
"""
from __future__ import annotations

import datetime as _dt
from decimal import Decimal

import numpy as np
import pandas as pd

from stock_backtest.backtest.engine import (
    AssetSpec,
    BacktestConfig,
    BacktestEngine,
    CASH_SYMBOL,
)
from stock_backtest.backtest.fx import FXConverter
from stock_backtest.config import Settings
from stock_backtest.strategies.base import Strategy, StrategyParams


class _DummyParams(StrategyParams):
    pass


class _CashSleeveStrategy(Strategy):
    """60% SPY + 40% _CASH_, rebalanced every period."""

    name = "_smoke_cash_sleeve"
    params_schema = _DummyParams
    description = "Smoke helper: SPY 0.6 + _CASH_ 0.4."

    def generate_weights(self, prices, rebalance_dates):
        rows = []
        for _ in rebalance_dates:
            rows.append({"SPY": 0.6, CASH_SYMBOL: 0.4})
        return pd.DataFrame(rows, index=rebalance_dates)

    def required_universe(self):
        # Intentionally include _CASH_; the engine must filter it out.
        return ["SPY", CASH_SYMBOL]


def _default_settings() -> Settings:
    return Settings.model_validate(
        {
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
                "enabled": False,
                "profile": "none",
                "profiles": {"none": {}},
            },
        }
    )


def _make_price_loader(sessions: pd.DatetimeIndex, asset_id: int):
    def _loader(universe, start, end):
        n = len(sessions)
        # Flat-ish price series so the arithmetic below is easy to eyeball.
        series = 100.0 * (1.0 + 0.0002 * np.arange(n))
        return pd.DataFrame({asset_id: pd.Series(series, index=sessions)})

    return _loader


def main() -> None:
    start = _dt.date(2023, 1, 3)
    end = _dt.date(2023, 6, 30)

    from stock_backtest.backtest.calendar import get_trading_days

    sessions = get_trading_days("US", start, end)

    spy = AssetSpec(
        asset_id=1,
        symbol="SPY",
        market="US",
        currency="USD",
        asset_class="overseas_etf",
        start_date=start,
        end_date=end,
    )
    # The user could accidentally pass _CASH_ as an AssetSpec; the engine
    # must strip it. Exercise that path.
    sneaky_cash = AssetSpec(
        asset_id=9999,
        symbol=CASH_SYMBOL,
        market="US",
        currency="USD",
        asset_class="overseas_etf",
        start_date=start,
        end_date=end,
    )

    config = BacktestConfig(
        strategy_name="_smoke_cash_sleeve",
        params={},
        universe=[spy, sneaky_cash],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )

    settings = _default_settings()
    price_loader = _make_price_loader(sessions, asset_id=1)
    fx_overrides = {}
    for ts in sessions:
        d = ts.date()
        fx_overrides[("USD", "KRW", d)] = Decimal("1350")
        fx_overrides[("KRW", "USD", d)] = Decimal("1") / Decimal("1350")
    fx = FXConverter(session=None, fx_spread_bps=20, rate_overrides=fx_overrides)

    engine = BacktestEngine(
        settings,
        session_factory=None,
        price_loader=price_loader,
        fx_converter=fx,
    )
    result = engine.run(config, _CashSleeveStrategy(_DummyParams()))

    # 1) No trade record should reference the cash pseudo-asset.
    for t in result.trades:
        assert t.asset_id != 9999, f"_CASH_ AssetSpec leaked into trade: {t}"
        # Cash moves should never appear as BUY/SELL: FX trades have
        # asset_id=None, BUY/SELL must be real assets.
        if t.side in ("BUY", "SELL"):
            assert t.asset_id == 1, f"Unexpected BUY/SELL asset: {t}"

    # 2) SPY trades must exist and sized ~ equity*0.6/price.
    buys = [t for t in result.trades if t.side == "BUY"]
    assert buys, "Expected at least one BUY for SPY"
    first_buy = buys[0]
    expected_qty = Decimal("100000") * Decimal("0.6") / Decimal("100")  # 600
    # Allow ~2% tolerance for the cost cushion + drift.
    ratio = float(first_buy.qty) / float(expected_qty)
    assert 0.95 <= ratio <= 1.05, (
        f"First BUY qty {first_buy.qty} not within 5% of expected {expected_qty}"
    )

    # 3) Final equity should be in the ballpark of 100k (0.6*SPY + 0.4*cash).
    final_equity = float(result.equity_curve.iloc[-1])
    assert 95_000 <= final_equity <= 110_000, (
        f"Unexpected final equity: {final_equity}"
    )

    print("trades emitted:", len(result.trades))
    print("first BUY qty:", first_buy.qty, "price:", first_buy.price)
    print("final equity:", final_equity)
    print("OK: _CASH_ sleeve handled without synthetic trades.")


if __name__ == "__main__":
    main()
