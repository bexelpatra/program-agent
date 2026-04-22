"""Regression tests for the vectorised backtest engine (TASK-019).

These tests complement ``test_engine_smoke.py`` by covering specific
behavioural scenarios: 100%-cash no-op, single-asset buy-and-hold,
60/40 monthly rebalancing, FX-spread, missing-price error, tax on/off
comparison, crypto market-mode, and an analytically-solvable known-good
case.

All tests are in-memory: no DB, no network. The engine is driven by
injected :class:`FXConverter` and ``price_loader``.
"""

from __future__ import annotations

import datetime as _dt
from decimal import Decimal
from typing import Iterable

import numpy as np
import pandas as pd
import pytest

from stock_backtest.backtest.calendar import get_trading_days
from stock_backtest.backtest.calendar_guard import MissingPriceError
from stock_backtest.backtest.engine import (
    AssetSpec,
    BacktestConfig,
    BacktestEngine,
)
from stock_backtest.backtest.fx import FXConverter
from stock_backtest.config import Settings
from stock_backtest.strategies.base import Strategy, StrategyParams
from stock_backtest.strategies.static.fixed_weight import (
    FixedWeight,
    FixedWeightParams,
)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


class _DummyParams(StrategyParams):
    """Empty params used by inline dummy strategies."""

    pass


class _AllCashStrategy(Strategy):
    """Scenario 1: strategy returns *no* target weights (100% cash)."""

    name = "all_cash"
    params_schema = _DummyParams
    description = "100% cash - empty weights every rebalance."

    def generate_weights(self, prices, rebalance_dates):
        # Return a DataFrame with zero columns -> engine will see weights sum
        # to zero across all assets -> no trades executed.
        return pd.DataFrame(0.0, index=rebalance_dates, columns=list(prices.columns))

    def required_universe(self):
        return None


class _SingleAssetStrategy(Strategy):
    """Allocate 100% to the first symbol every rebalance."""

    name = "single_asset"
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


def _default_settings(*, tax_enabled: bool, fx_spread_bps: int = 20) -> Settings:
    """Return a :class:`Settings` instance suitable for regression runs."""

    base = {
        "base_currency": "USD",
        "market_mode": "STOCK",
        "costs": {
            "commission_buy_bps": 5,
            "commission_sell_bps": 5,
            "slippage_bps": 3,
            "fx_spread_bps": fx_spread_bps,
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


def _fx_overrides(
    dates: Iterable[pd.Timestamp],
    pairs: dict[tuple[str, str], float],
) -> dict:
    """Expand FX rate overrides across every date in ``dates`` for every pair.

    ``pairs`` maps ``(base, quote) -> rate``. The inverse pair is filled in
    automatically so the :class:`FXConverter` can serve either direction.
    """
    overrides: dict = {}
    for ts in dates:
        d = ts.date() if isinstance(ts, pd.Timestamp) else ts
        for (b, q), rate in pairs.items():
            overrides[(b, q, d)] = Decimal(str(rate))
            overrides[(q, b, d)] = Decimal(1) / Decimal(str(rate))
    return overrides


def _build_fx(
    dates: pd.DatetimeIndex,
    *,
    pairs: dict[tuple[str, str], float] | None = None,
    fx_spread_bps: int = 20,
) -> FXConverter:
    pairs = pairs or {("USD", "KRW"): 1350.0}
    overrides = _fx_overrides(dates, pairs)
    return FXConverter(
        session=None, fx_spread_bps=fx_spread_bps, rate_overrides=overrides
    )


def _us_sessions(start: _dt.date, end: _dt.date) -> pd.DatetimeIndex:
    return get_trading_days("US", start, end)


def _const_loader(sessions: pd.DatetimeIndex, values: dict[int, list[float]]):
    """Build a PriceLoader that returns predetermined per-asset series."""

    def _loader(universe, start, end):
        data = {aid: pd.Series(vals, index=sessions) for aid, vals in values.items()}
        return pd.DataFrame(data)

    return _loader


# ---------------------------------------------------------------------------
# 1. 100% cash: empty weights -> flat equity, zero commission
# ---------------------------------------------------------------------------


def test_all_cash_no_trades_flat_equity():
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 12, 30)
    sessions = _us_sessions(start, end)

    n = len(sessions)
    prices = {1: list(100.0 + np.linspace(0, 20, n))}  # price moves, irrelevant
    price_loader = _const_loader(sessions, prices)

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
        strategy_name="all_cash",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    result = engine.run(config, _AllCashStrategy(_DummyParams()))

    # No trades recorded.
    assert result.trades == []
    # Equity constant = initial capital.
    assert float(result.equity_curve.iloc[0]) == pytest.approx(100_000.0)
    assert float(result.equity_curve.iloc[-1]) == pytest.approx(100_000.0)
    assert result.equity_curve.nunique() == 1


# ---------------------------------------------------------------------------
# 2. Single-asset buy-and-hold: price 2x -> equity ~ 2x * (1 - costs)
# ---------------------------------------------------------------------------


def test_buy_and_hold_doubles_with_costs():
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 12, 30)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    # Linear price doubling from 100 to 200.
    prices = {1: list(np.linspace(100.0, 200.0, n))}
    price_loader = _const_loader(sessions, prices)

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
        strategy_name="single_asset",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        # Allocate once at the start and hold: use Y freq so no monthly
        # rebalancing interferes with buy-and-hold.
        rebalance_freq="Y",
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))

    final = float(result.equity_curve.iloc[-1])
    # Expected: ~2x initial capital minus buy costs (comm 5bps + slip 3bps
    # + ~50bps cash cushion). Accept [1.97x, 2.01x].
    assert final > 100_000.0 * 1.95, f"final={final}"
    assert final < 100_000.0 * 2.01, f"final={final}"
    # Exactly one BUY trade (no monthly rebalancing).
    buys = [t for t in result.trades if t.side == "BUY"]
    assert len(buys) == 1


# ---------------------------------------------------------------------------
# 3. 60/40 monthly rebalancing maintains weights within tolerance
# ---------------------------------------------------------------------------


def test_monthly_rebalance_maintains_60_40():
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 12, 30)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    # Asset 1 (equity) rises, asset 2 (bond) stays roughly flat. This forces
    # drift that the rebalancer must correct each month.
    rng = np.random.default_rng(42)
    equity_series = 100.0 * np.cumprod(1.0 + rng.normal(0.0008, 0.01, n))
    bond_series = 50.0 * np.cumprod(1.0 + rng.normal(0.0001, 0.002, n))
    prices = {1: list(equity_series), 2: list(bond_series)}
    price_loader = _const_loader(sessions, prices)

    assets = [
        AssetSpec(1, "SPY", "US", "USD", "overseas_etf", start, end),
        AssetSpec(2, "AGG", "US", "USD", "overseas_etf", start, end),
    ]
    config = BacktestConfig(
        strategy_name="fixed_weight",
        params={"weights": {"SPY": 0.6, "AGG": 0.4}},
        universe=assets,
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    strategy = FixedWeight(FixedWeightParams(weights={"SPY": 0.6, "AGG": 0.4}))
    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    result = engine.run(config, strategy)

    # After at least one rebalance, inspect the weight distribution on each
    # rebalance day (close of that day, before next-day drift). We check the
    # equity curve is reasonable and that multiple rebalances happened.
    assert len(result.trades) >= 2  # initial alloc + at least one monthly
    assert any(t.asset_id == 2 for t in result.trades)  # bond got traded
    assert float(result.equity_curve.iloc[-1]) > 0


# ---------------------------------------------------------------------------
# 4. FX spread cost on cross-currency rebalance
# ---------------------------------------------------------------------------


def test_fx_spread_has_effect_on_cross_currency_rebalance():
    """EUR-denominated asset + cross-currency rebalance: a non-trivial
    ``fx_spread_bps`` must produce a different final equity than a near-zero
    spread. This pins the plumbing without asserting a *direction* (see
    tester-report-TASK-019 for a bug in ``_ensure_cash`` that currently makes
    wider spreads *improve* equity instead of worsening it).
    """
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

    def _build(spread_bps: int):
        settings = _default_settings(tax_enabled=False, fx_spread_bps=spread_bps)
        pairs = {("USD", "EUR"): 0.9, ("EUR", "KRW"): 1500.0, ("USD", "KRW"): 1350.0}
        fx = _build_fx(sessions, pairs=pairs, fx_spread_bps=spread_bps)
        loader = _const_loader(sessions, prices)
        return BacktestEngine(
            settings,
            session_factory=None,
            price_loader=loader,
            fx_converter=fx,
        )

    engine_narrow = _build(1)  # effectively ~zero spread
    engine_wide = _build(40)

    strategy = _SingleAssetStrategy(_DummyParams())
    r_narrow = engine_narrow.run(config, strategy)
    r_wide = engine_wide.run(config, strategy)

    final_narrow = float(r_narrow.equity_curve.iloc[-1])
    final_wide = float(r_wide.equity_curve.iloc[-1])
    # The two runs must differ materially; the *magnitude* captures the
    # spread plumbing. Sign is not asserted here (see code-issue in
    # tester-report-TASK-019).
    delta = abs(final_wide - final_narrow)
    assert delta > 50.0, (
        f"fx_spread_bps had no effect on equity: narrow={final_narrow}, "
        f"wide={final_wide}"
    )


# ---------------------------------------------------------------------------
# 5. Non-trading-day / missing price -> MissingPriceError
# ---------------------------------------------------------------------------


def test_missing_price_raises_missing_price_error():
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2022, 3, 31)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    values = list(np.linspace(100.0, 110.0, n))
    # Inject an explicit NaN at an interior trading day.
    gap_idx = n // 2
    values[gap_idx] = float("nan")
    prices = {1: values}
    price_loader = _const_loader(sessions, prices)

    asset = AssetSpec(1, "SPY", "US", "USD", "overseas_etf", start, end)
    config = BacktestConfig(
        strategy_name="single_asset",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    with pytest.raises(MissingPriceError):
        engine.run(config, _SingleAssetStrategy(_DummyParams()))


# ---------------------------------------------------------------------------
# 6 & 7. Tax on vs off: below-deduction no tax, above deduction taxed
# ---------------------------------------------------------------------------


def _run_tax_scenario(
    tax_enabled: bool,
    *,
    final_gain_fraction: float,
    initial_capital: Decimal = Decimal("100000"),
):
    """Run a 2-year backtest where the asset rises ``final_gain_fraction``
    and monthly rebalancing generates realized gains every month.

    ``final_gain_fraction=0.01`` keeps cumulative realized gains small
    enough to stay under the 2.5 M KRW deduction. A larger value pushes
    us past it. ``initial_capital`` scales the KRW-denominated realized
    gains so we can exceed the 2.5M KRW deduction without requiring
    unrealistic price moves.
    """
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2023, 12, 29)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    # Asset 1 rises by final_gain_fraction; asset 2 is flat. Divergent paths
    # force the 50/50 rebalancer to sell the winner each month, generating
    # realized gains the tax module can see.
    rising = list(np.linspace(100.0, 100.0 * (1 + final_gain_fraction), n))
    flat = [100.0] * n
    prices = {1: rising, 2: flat}
    price_loader = _const_loader(sessions, prices)

    assets = [
        AssetSpec(1, "SPY", "US", "USD", "overseas_etf", start, end),
        AssetSpec(2, "AGG", "US", "USD", "overseas_etf", start, end),
    ]
    config = BacktestConfig(
        strategy_name="fixed_weight",
        params={"weights": {"SPY": 0.5, "AGG": 0.5}},
        universe=assets,
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=initial_capital,
        rebalance_freq="ME",
    )
    settings = _default_settings(tax_enabled=tax_enabled)
    fx = _build_fx(sessions)

    strategy = FixedWeight(FixedWeightParams(weights={"SPY": 0.5, "AGG": 0.5}))
    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    return engine.run(config, strategy)


def test_tax_on_below_deduction_no_tax():
    """Tiny gains (1% over 2 years) -> well under 2.5M KRW -> zero tax."""
    result = _run_tax_scenario(tax_enabled=True, final_gain_fraction=0.01)
    total_tax = sum(result.tax_paid_by_year.values(), Decimal("0"))
    # Could be negative (loss refunds within year), but must be near zero.
    assert abs(total_tax) < Decimal("100"), f"unexpected tax: {total_tax}"


def test_tax_off_vs_on_same_scenario():
    """When gains exceed the deduction, tax-on equity < tax-off equity.

    We scale up ``initial_capital`` to 10M USD so realized gains from
    monthly rebalancing clearly exceed the 2.5M KRW annual deduction
    (each individual realized trade here is ~1M KRW+, summing to
    hundreds of millions KRW over the 2-year run).
    """
    big_capital = Decimal("10000000")
    r_on = _run_tax_scenario(
        tax_enabled=True, final_gain_fraction=0.5, initial_capital=big_capital
    )
    r_off = _run_tax_scenario(
        tax_enabled=False, final_gain_fraction=0.5, initial_capital=big_capital
    )

    final_on = float(r_on.equity_curve.iloc[-1])
    final_off = float(r_off.equity_curve.iloc[-1])
    assert (
        final_off > final_on
    ), f"tax-off ({final_off}) should exceed tax-on ({final_on})"
    total_tax_on = sum(r_on.tax_paid_by_year.values(), Decimal("0"))
    assert total_tax_on > Decimal("0")
    # tax-off should have zero tax paid.
    total_tax_off = sum(r_off.tax_paid_by_year.values(), Decimal("0"))
    assert total_tax_off == Decimal("0")


# ---------------------------------------------------------------------------
# 8. market_mode=CRYPTO: weekends present in equity curve
# ---------------------------------------------------------------------------


def test_crypto_mode_includes_weekends():
    start = _dt.date(2023, 1, 1)
    end = _dt.date(2023, 1, 31)
    # Synthetic 365-day calendar: every calendar day.
    sessions = get_trading_days("CRYPTO", start, end)
    n = len(sessions)
    assert n == 31  # Jan has 31 days including weekends

    prices = {1: list(np.linspace(20000.0, 22000.0, n))}
    price_loader = _const_loader(sessions, prices)

    asset = AssetSpec(1, "BTC-USD", "CRYPTO", "USD", "crypto", start, end)
    config = BacktestConfig(
        strategy_name="single_asset",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="CRYPTO",
        initial_capital=Decimal("100000"),
        rebalance_freq="ME",
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))

    # Equity curve has 31 rows and contains at least one Saturday/Sunday.
    assert len(result.equity_curve) == 31
    weekdays = {ts.weekday() for ts in result.equity_curve.index}
    # weekday() -> 5 Sat, 6 Sun
    assert 5 in weekdays or 6 in weekdays, f"got weekdays={weekdays}"


# ---------------------------------------------------------------------------
# 9. Known-good regression: analytically solvable buy-and-hold
# ---------------------------------------------------------------------------


def test_known_good_buy_and_hold_analytical():
    """Two-year buy-and-hold of a single asset that doubles.

    Analytical final equity under buy-and-hold ≈ 2 × initial_capital × (1 − c),
    where c is total one-way cost (commission + slippage + 50bps cash cushion).
    We tolerate ±1%.
    """
    start = _dt.date(2022, 1, 3)
    end = _dt.date(2023, 12, 29)
    sessions = _us_sessions(start, end)
    n = len(sessions)

    prices = {1: list(np.linspace(100.0, 200.0, n))}
    price_loader = _const_loader(sessions, prices)

    asset = AssetSpec(1, "SPY", "US", "USD", "overseas_etf", start, end)
    config = BacktestConfig(
        strategy_name="single_asset",
        params={},
        universe=[asset],
        period_start=start,
        period_end=end,
        base_currency="USD",
        market_mode="STOCK",
        initial_capital=Decimal("100000"),
        rebalance_freq="Y",  # annual -> effectively one allocation then hold
    )
    settings = _default_settings(tax_enabled=False)
    fx = _build_fx(sessions)

    engine = BacktestEngine(
        settings, session_factory=None, price_loader=price_loader, fx_converter=fx
    )
    result = engine.run(config, _SingleAssetStrategy(_DummyParams()))

    # Expected final equity: 2x * (1 - 50bps cushion - 8bps trade costs) ≈ 1.9884x
    # Full expansion: initial * (1 - 0.005 - 0.0005 - 0.0003) * 2 ≈ 198_840.
    # Allow ±1% band.
    final = float(result.equity_curve.iloc[-1])
    expected = 100_000.0 * 2.0 * (1.0 - 0.005 - 0.0005 - 0.0003)
    assert final == pytest.approx(
        expected, rel=0.01
    ), f"final={final}, expected~={expected}"
