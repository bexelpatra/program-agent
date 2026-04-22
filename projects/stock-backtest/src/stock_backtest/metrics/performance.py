"""Performance metrics for backtest results.

Computes standard risk/return metrics from an equity curve (and optional
trade records). All internal math is done in ``float``; :class:`Decimal`
inputs are coerced via ``float(...)``.

Typical usage:

>>> from stock_backtest.metrics.performance import compute_all
>>> stats = compute_all(result.equity_curve, trades=result.trades)

The public surface is:

- :func:`cagr`
- :func:`annualized_volatility`
- :func:`sharpe_ratio`
- :func:`sortino_ratio`
- :func:`max_drawdown`
- :func:`calmar_ratio`
- :func:`turnover`
- :func:`win_rate`
- :func:`compute_all`
"""

from __future__ import annotations

import math
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, Sequence

import numpy as np
import pandas as pd

if TYPE_CHECKING:  # pragma: no cover
    from stock_backtest.backtest.engine import TradeRecord


__all__ = [
    "cagr",
    "annualized_volatility",
    "sharpe_ratio",
    "sortino_ratio",
    "max_drawdown",
    "calmar_ratio",
    "turnover",
    "win_rate",
    "compute_all",
    "to_returns",
]

_TRADING_DAYS = 252


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _as_float_series(equity: pd.Series) -> pd.Series:
    """Coerce an equity series to a clean float64 series.

    Accepts objects containing :class:`Decimal` by running through ``float``.
    Drops NaN leading/trailing values but keeps ordering.
    """
    if not isinstance(equity, pd.Series):
        equity = pd.Series(equity)
    if equity.dtype == object:
        equity = equity.map(lambda v: float(v) if v is not None else np.nan)
    return equity.astype("float64")


def _years_span(equity: pd.Series) -> float:
    """Return the elapsed years between the first and last index of ``equity``.

    Falls back to ``len(equity) / 252`` when the index is not datetime-like.
    """
    if len(equity) < 2:
        return 0.0
    idx = equity.index
    if isinstance(idx, pd.DatetimeIndex):
        delta = idx[-1] - idx[0]
        return max(delta.days / 365.25, 0.0)
    return (len(equity) - 1) / _TRADING_DAYS


def to_returns(equity: pd.Series) -> pd.Series:
    """Simple (arithmetic) daily returns, with the first NaN dropped."""
    eq = _as_float_series(equity)
    if len(eq) < 2:
        return pd.Series(dtype="float64")
    rets = eq.pct_change().dropna()
    # Replace inf (division by 0 equity) with NaN then drop.
    rets = rets.replace([np.inf, -np.inf], np.nan).dropna()
    return rets


# ---------------------------------------------------------------------------
# Metric functions
# ---------------------------------------------------------------------------


def cagr(equity: pd.Series) -> float:
    """Compound annual growth rate.

    Returns 0.0 for empty/single-point series or for non-positive start/end
    equity.
    """
    eq = _as_float_series(equity).dropna()
    if len(eq) < 2:
        return 0.0
    start = float(eq.iloc[0])
    end = float(eq.iloc[-1])
    years = _years_span(eq)
    if years <= 0 or start <= 0:
        return 0.0
    if end <= 0:
        # Terminal ruin: treat as -100% CAGR.
        return -1.0
    return (end / start) ** (1.0 / years) - 1.0


def annualized_volatility(
    returns: pd.Series, periods_per_year: int = _TRADING_DAYS
) -> float:
    """Annualised standard deviation of ``returns``.

    Uses the sample standard deviation (``ddof=1``). Returns 0.0 if fewer
    than 2 observations remain after cleaning.
    """
    r = _as_float_series(returns).dropna()
    if len(r) < 2:
        return 0.0
    return float(r.std(ddof=1) * math.sqrt(periods_per_year))


def sharpe_ratio(
    returns: pd.Series,
    risk_free_annual: float = 0.0,
    periods_per_year: int = _TRADING_DAYS,
) -> float:
    """Annualised Sharpe ratio.

    Returns ``+inf`` / ``-inf`` when the excess-return std is 0 but the mean
    excess return is non-zero. Returns 0.0 when both mean and std are 0.
    """
    r = _as_float_series(returns).dropna()
    if len(r) < 2:
        return 0.0
    rf_per_period = (1.0 + risk_free_annual) ** (1.0 / periods_per_year) - 1.0
    excess = r - rf_per_period
    mean = float(excess.mean())
    std = float(excess.std(ddof=1))
    if std == 0 or math.isnan(std):
        if mean == 0:
            return 0.0
        return math.inf if mean > 0 else -math.inf
    return (mean / std) * math.sqrt(periods_per_year)


def sortino_ratio(
    returns: pd.Series,
    risk_free_annual: float = 0.0,
    periods_per_year: int = _TRADING_DAYS,
) -> float:
    """Annualised Sortino ratio (downside-only std of excess returns)."""
    r = _as_float_series(returns).dropna()
    if len(r) < 2:
        return 0.0
    rf_per_period = (1.0 + risk_free_annual) ** (1.0 / periods_per_year) - 1.0
    excess = r - rf_per_period
    mean = float(excess.mean())
    downside = excess[excess < 0]
    if len(downside) == 0:
        if mean == 0:
            return 0.0
        return math.inf if mean > 0 else -math.inf
    # Root-mean-square of negative excess returns (population-style: divide
    # by the count of all periods is an alternative convention, but the
    # standard Sortino uses the downside deviation computed against a
    # target, here the risk-free rate, with ddof=0 on the downside subset).
    dd = math.sqrt(float((downside**2).mean()))
    if dd == 0:
        return math.inf if mean > 0 else (-math.inf if mean < 0 else 0.0)
    return (mean / dd) * math.sqrt(periods_per_year)


def max_drawdown(equity: pd.Series) -> float:
    """Return the maximum drawdown as a negative number (e.g. ``-0.32``).

    Returns 0.0 for a monotonically non-decreasing series or for series
    with fewer than 2 points.
    """
    eq = _as_float_series(equity).dropna()
    if len(eq) < 2:
        return 0.0
    running_max = eq.cummax()
    # Guard against zero/neg running max (should not happen for positive
    # equity, but be defensive).
    with np.errstate(divide="ignore", invalid="ignore"):
        dd = (eq - running_max) / running_max
    dd = dd.replace([np.inf, -np.inf], np.nan).dropna()
    if len(dd) == 0:
        return 0.0
    mdd = float(dd.min())
    return min(mdd, 0.0)


def calmar_ratio(equity: pd.Series) -> float:
    """CAGR divided by absolute max drawdown.

    Returns ``+inf`` when MDD is 0 and CAGR is positive, ``-inf`` when CAGR
    is negative with 0 MDD, and 0.0 when both are 0.
    """
    c = cagr(equity)
    mdd = max_drawdown(equity)
    if mdd == 0:
        if c == 0:
            return 0.0
        return math.inf if c > 0 else -math.inf
    return c / abs(mdd)


def turnover(
    trades: Sequence["TradeRecord"] | None,
    equity: pd.Series,
) -> float:
    """Annualised turnover.

    Defined as ``sum(|trade notional|) / mean(equity) / years``.  Returns
    0.0 for empty trade lists or empty equity.
    """
    if not trades:
        return 0.0
    eq = _as_float_series(equity).dropna()
    if len(eq) == 0:
        return 0.0
    mean_eq = float(eq.mean())
    if mean_eq <= 0:
        return 0.0
    years = _years_span(eq)
    if years <= 0:
        years = max(len(eq) / _TRADING_DAYS, 1.0 / _TRADING_DAYS)

    total_notional = 0.0
    for t in trades:
        # Skip FX conversion rows: their ``qty * price`` is a source-currency
        # notional times an FX rate, not an asset notional, so including them
        # would distort turnover.
        if getattr(t, "side", None) == "FX":
            continue
        qty = float(getattr(t, "qty", 0) or 0)
        price = float(getattr(t, "price", 0) or 0)
        total_notional += abs(qty * price)
    return (total_notional / mean_eq) / years


def win_rate(
    trades_or_returns: Sequence["TradeRecord"] | pd.Series | Iterable[float],
) -> float:
    """Proportion of positive values.

    - If given a :class:`pandas.Series` or iterable of numbers, counts the
      fraction strictly greater than 0.
    - If given a sequence of :class:`TradeRecord`-like objects (duck-typed
      via ``qty`` + ``price`` attributes), the notion of "win" is not well
      defined without PnL, so we fall back to returning 0.0.  Callers with
      realised-trade PnL should pass a Series instead.
    """
    if trades_or_returns is None:
        return 0.0
    if isinstance(trades_or_returns, pd.Series):
        values = _as_float_series(trades_or_returns).dropna()
        if len(values) == 0:
            return 0.0
        return float((values > 0).sum()) / float(len(values))
    # Try generic iterable of numbers; if items look like TradeRecord
    # (have .qty/.price but no .pnl), we cannot score them.
    items = list(trades_or_returns)
    if not items:
        return 0.0
    first = items[0]
    if hasattr(first, "qty") and hasattr(first, "price") and not hasattr(first, "pnl"):
        return 0.0
    try:
        nums = [float(x) for x in items]
    except (TypeError, ValueError):
        return 0.0
    if not nums:
        return 0.0
    wins = sum(1 for v in nums if v > 0)
    return wins / len(nums)


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------


def compute_all(
    equity: pd.Series,
    trades: Sequence["TradeRecord"] | None = None,
    risk_free_annual: float = 0.0,
    trading_days_per_year: int = _TRADING_DAYS,
) -> dict[str, float]:
    """Compute the full bundle of metrics in one pass.

    Parameters
    ----------
    equity:
        Equity curve indexed by date. Values may be Decimal or float.
    trades:
        Optional trade list for turnover.
    risk_free_annual:
        Annual risk-free rate used by Sharpe and Sortino.
    trading_days_per_year:
        Annualisation factor (default 252).
    """
    eq = _as_float_series(equity)
    if len(eq.dropna()) < 2:
        # Degenerate equity: emit a zero-filled bundle so callers don't crash.
        return {
            "cagr": 0.0,
            "annualized_volatility": 0.0,
            "sharpe_ratio": 0.0,
            "sortino_ratio": 0.0,
            "max_drawdown": 0.0,
            "calmar_ratio": 0.0,
            "turnover": 0.0,
            "win_rate": 0.0,
        }
    rets = to_returns(eq)
    return {
        "cagr": cagr(eq),
        "annualized_volatility": annualized_volatility(rets, trading_days_per_year),
        "sharpe_ratio": sharpe_ratio(rets, risk_free_annual, trading_days_per_year),
        "sortino_ratio": sortino_ratio(rets, risk_free_annual, trading_days_per_year),
        "max_drawdown": max_drawdown(eq),
        "calmar_ratio": calmar_ratio(eq),
        "turnover": turnover(trades, eq),
        "win_rate": win_rate(rets),
    }
