"""Tests for :mod:`stock_backtest.metrics.performance`."""

from __future__ import annotations

import datetime as _dt
import math
from decimal import Decimal

import numpy as np
import pandas as pd
import pytest

from stock_backtest.metrics.performance import (
    annualized_volatility,
    cagr,
    calmar_ratio,
    compute_all,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
    to_returns,
    turnover,
    win_rate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _daily_index(n: int, start: str = "2020-01-01") -> pd.DatetimeIndex:
    return pd.date_range(start=start, periods=n, freq="D")


def _compounded_equity(annual_return: float, days: int = 252) -> pd.Series:
    """Build an equity curve that compounds to exactly ``annual_return`` over
    ``days`` calendar days."""
    per_period = (1 + annual_return) ** (1 / days) - 1
    idx = _daily_index(days + 1)
    vals = [100.0 * (1 + per_period) ** i for i in range(days + 1)]
    return pd.Series(vals, index=idx)


# ---------------------------------------------------------------------------
# Known-value tests: straight-line 10% / year
# ---------------------------------------------------------------------------


def test_cagr_ten_percent_straight_line():
    eq = _compounded_equity(0.10, days=252)
    # Span is 252 days ≈ 0.69 years, but CAGR uses actual year fraction and
    # the compounding was calibrated against 252 days directly, so we compute
    # via the same formula to check consistency.
    years = (eq.index[-1] - eq.index[0]).days / 365.25
    expected = (eq.iloc[-1] / eq.iloc[0]) ** (1 / years) - 1
    assert cagr(eq) == pytest.approx(expected, rel=1e-9)


def test_max_drawdown_monotonic_is_zero():
    eq = _compounded_equity(0.10, days=252)
    assert max_drawdown(eq) == 0.0


def test_sharpe_of_constant_return_is_very_large():
    # All returns equal (up to float-compounding noise) -> std ~ 0, huge Sharpe.
    eq = _compounded_equity(0.10, days=252)
    rets = to_returns(eq)
    sr = sharpe_ratio(rets, risk_free_annual=0.0)
    assert sr > 1e6

    # A zero-mean zero-variance input should yield exactly 0.
    zeros = pd.Series([0.0, 0.0, 0.0, 0.0])
    assert sharpe_ratio(zeros) == 0.0


def test_calmar_ratio_no_drawdown_infinite():
    eq = _compounded_equity(0.10, days=252)
    cr = calmar_ratio(eq)
    assert math.isinf(cr) and cr > 0


# ---------------------------------------------------------------------------
# Synthetic series with real volatility
# ---------------------------------------------------------------------------


def _synthetic_series(seed: int = 42, n: int = 1000) -> pd.Series:
    rng = np.random.default_rng(seed)
    rets = rng.normal(loc=0.0005, scale=0.012, size=n)
    eq = 100.0 * np.cumprod(1 + rets)
    return pd.Series(eq, index=_daily_index(n))


def test_synthetic_mdd_is_negative():
    eq = _synthetic_series()
    mdd = max_drawdown(eq)
    assert mdd < 0
    assert mdd > -1.0  # Sanity: not ruin


def test_synthetic_sharpe_reasonable():
    eq = _synthetic_series()
    rets = to_returns(eq)
    sr = sharpe_ratio(rets, risk_free_annual=0.0)
    # With mean=0.0005 daily, std=0.012 daily, annualised Sharpe ≈
    # (0.0005/0.012) * sqrt(252) ≈ 0.66. Realised value depends on seed;
    # allow a wide sanity band.
    assert 0.0 < sr < 2.0


def test_synthetic_sortino_finite_and_positive():
    eq = _synthetic_series()
    rets = to_returns(eq)
    so = sortino_ratio(rets)
    # With a positive-drift generator, Sortino should be finite and positive
    # in the same rough magnitude band as Sharpe.
    assert math.isfinite(so)
    assert 0.0 < so < 3.0


def test_annualized_vol_matches_manual():
    eq = _synthetic_series()
    rets = to_returns(eq)
    vol = annualized_volatility(rets)
    manual = rets.std(ddof=1) * math.sqrt(252)
    assert vol == pytest.approx(manual, rel=1e-12)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_empty_equity_returns_zero_bundle():
    out = compute_all(pd.Series(dtype="float64"))
    assert out["cagr"] == 0.0
    assert out["max_drawdown"] == 0.0
    assert out["sharpe_ratio"] == 0.0


def test_single_sample_equity():
    eq = pd.Series([100.0], index=_daily_index(1))
    assert cagr(eq) == 0.0
    assert max_drawdown(eq) == 0.0
    assert annualized_volatility(to_returns(eq)) == 0.0


def test_negative_final_equity_gives_minus_one_cagr():
    idx = _daily_index(3)
    eq = pd.Series([100.0, 50.0, -1.0], index=idx)
    # Our definition returns -1.0 (terminal ruin sentinel).
    assert cagr(eq) == -1.0


def test_decimal_input_is_coerced():
    idx = _daily_index(5)
    eq = pd.Series(
        [
            Decimal("100"),
            Decimal("101"),
            Decimal("102"),
            Decimal("103"),
            Decimal("104"),
        ],
        index=idx,
    )
    bundle = compute_all(eq)
    assert bundle["max_drawdown"] == 0.0
    assert bundle["cagr"] > 0


def test_mdd_known_value():
    # 100 -> 120 -> 60 -> 90. Peak=120, trough=60 -> mdd = (60-120)/120 = -0.5
    idx = _daily_index(4)
    eq = pd.Series([100.0, 120.0, 60.0, 90.0], index=idx)
    assert max_drawdown(eq) == pytest.approx(-0.5)


def test_win_rate_on_returns():
    rets = pd.Series([0.01, -0.005, 0.002, 0.0, -0.01, 0.007])
    # Positive: 0.01, 0.002, 0.007 -> 3 of 6 = 0.5
    assert win_rate(rets) == pytest.approx(0.5)


def test_win_rate_empty_returns_zero():
    assert win_rate([]) == 0.0
    assert win_rate(pd.Series(dtype="float64")) == 0.0


def test_turnover_empty_trades_is_zero():
    eq = _synthetic_series()
    assert turnover([], eq) == 0.0
    assert turnover(None, eq) == 0.0


def test_turnover_basic_math():
    from stock_backtest.backtest.engine import TradeRecord

    idx = _daily_index(252 + 1)
    eq = pd.Series(np.full(len(idx), 1000.0), index=idx)  # mean = 1000
    trades = [
        TradeRecord(
            date=_dt.date(2020, 1, 1),
            asset_id=1,
            side="BUY",
            qty=Decimal("10"),
            price=Decimal("50"),
            currency="USD",
            commission_bps=Decimal("15"),
            slippage_bps=Decimal("5"),
        ),
        TradeRecord(
            date=_dt.date(2020, 7, 1),
            asset_id=1,
            side="SELL",
            qty=Decimal("10"),
            price=Decimal("60"),
            currency="USD",
            commission_bps=Decimal("15"),
            slippage_bps=Decimal("5"),
        ),
    ]
    # Total notional = 10*50 + 10*60 = 1100. mean_eq=1000. years ~ 252/365.25.
    years = (idx[-1] - idx[0]).days / 365.25
    expected = (1100.0 / 1000.0) / years
    assert turnover(trades, eq) == pytest.approx(expected, rel=1e-9)


def test_sharpe_zero_variance_zero_mean_returns_zero():
    rets = pd.Series([0.0, 0.0, 0.0, 0.0])
    assert sharpe_ratio(rets) == 0.0


def test_sortino_no_downside_infinite_for_positive_mean():
    rets = pd.Series([0.01, 0.02, 0.005, 0.015])
    so = sortino_ratio(rets)
    assert math.isinf(so) and so > 0


def test_compute_all_keys():
    eq = _synthetic_series()
    out = compute_all(eq, trades=None, risk_free_annual=0.02)
    expected_keys = {
        "cagr",
        "annualized_volatility",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown",
        "calmar_ratio",
        "turnover",
        "win_rate",
    }
    assert set(out.keys()) == expected_keys
    for k, v in out.items():
        assert isinstance(v, float), f"{k} is not a float: {type(v)}"


def test_nan_returns_filtered():
    eq = pd.Series([100.0, np.nan, 101.0, 102.0], index=_daily_index(4))
    r = to_returns(eq)
    # NaN in the middle produces two NaNs in pct_change: they must be dropped.
    assert r.isna().sum() == 0
    assert len(r) >= 1
