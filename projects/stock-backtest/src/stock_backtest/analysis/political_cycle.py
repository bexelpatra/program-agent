"""Event-based seasonality analysis.

Complements :mod:`stock_backtest.analysis.seasonality` which handles the
calendar-only effects (month / day-of-week / month-edge / Sell-in-May /
Halloween).  This module focuses on **event-conditioned** effects:

- :func:`presidential_term_year_effect`
- :func:`election_year_effect`
- :func:`fomc_week_effect`
- :func:`earnings_season_effect`

All functions expect a daily-return :class:`pandas.Series` indexed by a
:class:`pandas.DatetimeIndex`.  Event inputs are either a DataFrame with
an ``event_date`` column (as returned from the ``market_events`` table)
or a :class:`pandas.DatetimeIndex` of dates.

NaN values in the input returns are dropped prior to grouping.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "presidential_term_year_effect",
    "election_year_effect",
    "fomc_week_effect",
    "earnings_season_effect",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _ensure_dt_series(returns: pd.Series) -> pd.Series:
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise ValueError(
            f"returns must have a DatetimeIndex, got " f"{type(returns.index).__name__}"
        )
    return returns.sort_index().dropna()


def _to_datetime_index(events) -> pd.DatetimeIndex:
    """Normalize event inputs to a sorted, unique :class:`DatetimeIndex`."""
    if isinstance(events, pd.DatetimeIndex):
        idx = events
    elif isinstance(events, pd.DataFrame):
        if "event_date" not in events.columns:
            raise ValueError("events DataFrame must contain an 'event_date' column")
        idx = pd.DatetimeIndex(pd.to_datetime(events["event_date"]))
    elif isinstance(events, pd.Series):
        idx = pd.DatetimeIndex(pd.to_datetime(events))
    else:
        idx = pd.DatetimeIndex(pd.to_datetime(list(events)))
    return idx.sort_values().unique()


def _group_stats(returns: pd.Series, by: pd.Series) -> pd.DataFrame:
    """Return mean / annualized / count / win_rate grouped by ``by``."""
    df = pd.DataFrame({"ret": returns.values, "grp": by}, index=returns.index)
    grouped = df.groupby("grp")["ret"]
    stats = grouped.agg(
        mean_daily="mean",
        count="count",
        win_rate=lambda x: float((x > 0).mean()) if len(x) else np.nan,
    )
    stats["annualized"] = (1.0 + stats["mean_daily"]) ** 252 - 1.0
    return stats[["mean_daily", "annualized", "count", "win_rate"]]


def _welch_t(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    nx, ny = x.size, y.size
    if nx < 2 or ny < 2:
        return float("nan")
    vx = x.var(ddof=1)
    vy = y.var(ddof=1)
    denom = np.sqrt(vx / nx + vy / ny)
    if denom == 0 or not np.isfinite(denom):
        return float("nan")
    return float((x.mean() - y.mean()) / denom)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def presidential_term_year_effect(
    returns: pd.Series, elections: pd.DataFrame | pd.DatetimeIndex
) -> pd.DataFrame:
    """Average daily return by US presidential-term year (1..4).

    For each date in ``returns``, the term year is computed as
    ``((date.year - last_election.year) % 4) + 1`` using the most recent
    election whose date is **on or before** the given date.  Dates
    preceding the earliest election are dropped.

    Parameters
    ----------
    returns : pd.Series
        Daily returns with DatetimeIndex.
    elections : pd.DataFrame | pd.DatetimeIndex
        US presidential election dates (DataFrame with ``event_date`` or
        a DatetimeIndex).

    Returns
    -------
    pd.DataFrame
        index = ``term_year`` (1..4),
        columns = ``[mean_daily, annualized, count, win_rate]``.
    """
    r = _ensure_dt_series(returns)
    elec = _to_datetime_index(elections)
    if len(elec) == 0:
        raise ValueError("elections is empty")

    election_years = pd.Series(elec.year.to_numpy(), index=elec)
    # For each date in r.index, find the most recent election year <= that date.
    pos = election_years.index.searchsorted(r.index, side="right") - 1
    valid = pos >= 0
    dropped = (~valid).sum()
    if dropped:
        r = r.iloc[valid]
        pos = pos[valid]
    last_election_years = election_years.values[pos]
    term_year = ((r.index.year.to_numpy() - last_election_years) % 4) + 1

    stats = _group_stats(r, pd.Series(term_year, index=r.index))
    stats = stats.reindex([1, 2, 3, 4])
    stats["count"] = stats["count"].fillna(0).astype(int)
    stats.index.name = "term_year"
    return stats


def election_year_effect(
    returns: pd.Series,
    elections: pd.DataFrame | pd.DatetimeIndex,
    midterms: pd.DataFrame | pd.DatetimeIndex,
) -> pd.DataFrame:
    """Compare returns in presidential / midterm / non-election years.

    A year is labelled:
    - ``presidential`` if the year matches any election year,
    - ``midterm`` if it matches any midterm year,
    - ``non_election`` otherwise.

    Parameters
    ----------
    returns : pd.Series
        Daily returns with DatetimeIndex.
    elections : pd.DataFrame | pd.DatetimeIndex
        US presidential election dates.
    midterms : pd.DataFrame | pd.DatetimeIndex
        US midterm election dates.

    Returns
    -------
    pd.DataFrame
        index = ``year_type`` in [``presidential``, ``midterm``,
        ``non_election``],
        columns = ``[mean_daily, annualized, count, win_rate]``.
    """
    r = _ensure_dt_series(returns)
    pres_years = set(_to_datetime_index(elections).year.tolist())
    mid_years = set(_to_datetime_index(midterms).year.tolist())

    def classify(y: int) -> str:
        if y in pres_years:
            return "presidential"
        if y in mid_years:
            return "midterm"
        return "non_election"

    labels = pd.Series([classify(y) for y in r.index.year], index=r.index)
    stats = _group_stats(r, labels)
    stats = stats.reindex(["presidential", "midterm", "non_election"])
    stats["count"] = stats["count"].fillna(0).astype(int)
    stats.index.name = "year_type"
    return stats


def fomc_week_effect(
    returns: pd.Series, fomc_dates: pd.DataFrame | pd.DatetimeIndex
) -> pd.DataFrame:
    """FOMC-meeting week vs. non-FOMC week daily returns.

    A "week" is identified by ISO year-week (``.isocalendar()``).  Weeks
    that contain any FOMC meeting date in ``fomc_dates`` are tagged
    ``fomc_week``; all other weeks are ``other_week``.

    Parameters
    ----------
    returns : pd.Series
        Daily returns with DatetimeIndex.
    fomc_dates : pd.DataFrame | pd.DatetimeIndex
        FOMC meeting dates.

    Returns
    -------
    pd.DataFrame
        index = ``week_type`` in [``fomc_week``, ``other_week``],
        columns = ``[mean_daily, annualized, count, win_rate, t_stat]``.
        ``t_stat`` is the Welch t-statistic fomc_week vs other_week and
        is identical in both rows (for readability).
    """
    r = _ensure_dt_series(returns)
    fomc = _to_datetime_index(fomc_dates)

    iso = r.index.isocalendar()
    # Key each day by (iso_year, iso_week)
    week_key = list(zip(iso.year.to_numpy(), iso.week.to_numpy()))

    fomc_iso = pd.DatetimeIndex(fomc).isocalendar()
    fomc_weeks = set(zip(fomc_iso.year.to_numpy(), fomc_iso.week.to_numpy()))

    labels = pd.Series(
        ["fomc_week" if k in fomc_weeks else "other_week" for k in week_key],
        index=r.index,
    )
    stats = _group_stats(r, labels)
    stats = stats.reindex(["fomc_week", "other_week"])
    stats["count"] = stats["count"].fillna(0).astype(int)
    stats.index.name = "week_type"

    fomc_vals = r[labels == "fomc_week"].to_numpy()
    other_vals = r[labels == "other_week"].to_numpy()
    t = _welch_t(fomc_vals, other_vals)
    stats["t_stat"] = t
    return stats


def earnings_season_effect(
    returns: pd.Series,
    earnings_dates: pd.DataFrame | pd.DatetimeIndex,
    window: int = 5,
) -> pd.DataFrame:
    """Returns within +-``window`` trading days of earnings-season peaks.

    Each date in ``returns`` is labelled ``in_window`` if it lies within
    ``window`` **trading days** (i.e. index positions in ``returns``) of
    any earnings-season peak date, otherwise ``out_window``.

    Parameters
    ----------
    returns : pd.Series
        Daily returns with DatetimeIndex.
    earnings_dates : pd.DataFrame | pd.DatetimeIndex
        Earnings-season peak dates.
    window : int, default 5
        Half-width of the neighbourhood in trading days (>=0).

    Returns
    -------
    pd.DataFrame
        index = ``bucket`` in [``in_window``, ``out_window``],
        columns = ``[mean_daily, annualized, count, win_rate, t_stat]``.
    """
    if window < 0:
        raise ValueError("window must be >= 0")
    r = _ensure_dt_series(returns)
    peaks = _to_datetime_index(earnings_dates)

    mask = np.zeros(len(r), dtype=bool)
    n = len(r)
    # For each peak, find nearest trading day in r.index and flag +-window.
    if n > 0 and len(peaks) > 0:
        positions = r.index.searchsorted(peaks, side="left")
        for p in positions:
            # p may be == n (peak after last date); clamp
            center = min(max(int(p), 0), n - 1)
            lo = max(0, center - window)
            hi = min(n - 1, center + window)
            mask[lo : hi + 1] = True

    labels = pd.Series(np.where(mask, "in_window", "out_window"), index=r.index)
    stats = _group_stats(r, labels)
    stats = stats.reindex(["in_window", "out_window"])
    stats["count"] = stats["count"].fillna(0).astype(int)
    stats.index.name = "bucket"

    in_vals = r[labels == "in_window"].to_numpy()
    out_vals = r[labels == "out_window"].to_numpy()
    stats["t_stat"] = _welch_t(in_vals, out_vals)
    return stats
