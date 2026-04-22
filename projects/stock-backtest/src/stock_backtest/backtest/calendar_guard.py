"""Non-trading-day defences for the backtest engine and repository layer.

Architecture decision #13 (``signal/stock-backtest/architecture.md``) mandates
a multi-layer defence against silently treating non-trading days (or missing
OHLCV rows) as zero-return observations. This module provides the shared
utilities used by the backtest engine and (in a future task) the repository
layer.

Design goals
------------
- **No silent zeros.** Any date that the calendar says is a session but has no
  price row must raise, not be filled with 0.
- **Alignment helpers.** When callers pass a non-trading day, offer explicit
  opt-in alignment to the previous or next session rather than guessing.
- **Vectorised.** ``align_to_trading_day`` and ``assert_universe_coverage``
  accept pandas structures and avoid Python-level loops over dates.

Public API
----------
- :class:`NonTradingDayError`, :class:`MissingPriceError` -- domain errors
  carrying the offending market/date/asset for precise diagnostics.
- :func:`validate_trading_day` -- scalar check with ``error|previous|next``
  alignment modes.
- :func:`validate_date_range` -- ensure a given price index covers every
  session of ``market`` in ``[start, end]``.
- :func:`align_to_trading_day` -- vectorised mapping of an arbitrary
  ``DatetimeIndex`` to sessions of a single market.
- :func:`assert_universe_coverage` -- per-asset coverage check across
  heterogeneous markets.

All functions accept and return tz-naive, midnight-normalised timestamps so
that they compose cleanly with :mod:`stock_backtest.backtest.calendar`.
"""

from __future__ import annotations

import datetime as _dt
import logging
from typing import Literal

import numpy as np
import pandas as pd

from .calendar import (
    get_trading_days,
    is_trading_day,
    next_trading_day,
    previous_trading_day,
)

__all__ = [
    "NonTradingDayError",
    "MissingPriceError",
    "validate_trading_day",
    "validate_date_range",
    "align_to_trading_day",
    "assert_universe_coverage",
]

_logger = logging.getLogger(__name__)

_AlignMode = Literal["error", "previous", "next"]
_Direction = Literal["previous", "next"]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------
class NonTradingDayError(ValueError):
    """Raised when a date is not a trading day for the requested market.

    Attributes
    ----------
    market:
        Market code that was queried.
    date:
        The offending :class:`datetime.date`.
    """

    def __init__(self, market: str, d: _dt.date, message: str | None = None) -> None:
        self.market = market
        self.date = d
        super().__init__(
            message or f"{d.isoformat()} is not a trading day for market {market!r}"
        )


class MissingPriceError(ValueError):
    """Raised when a trading day has no OHLCV row for an asset.

    Attributes
    ----------
    asset_id:
        Identifier of the asset (``None`` when the error is raised from a
        context without a single-asset attribution, e.g.
        :func:`validate_date_range`).
    date:
        The first date for which price data is missing.
    """

    def __init__(
        self,
        asset_id: int | None,
        d: _dt.date,
        message: str | None = None,
    ) -> None:
        self.asset_id = asset_id
        self.date = d
        default = f"Missing price on {d.isoformat()}" + (
            f" for asset_id={asset_id}" if asset_id is not None else ""
        )
        super().__init__(message or default)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _to_date(d: _dt.date | _dt.datetime | pd.Timestamp | str) -> _dt.date:
    if isinstance(d, pd.Timestamp):
        return d.date()
    if isinstance(d, _dt.datetime):
        return d.date()
    if isinstance(d, _dt.date):
        return d
    return pd.Timestamp(d).date()


def _normalize_index(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Return ``index`` as tz-naive, midnight-normalised ``DatetimeIndex``."""
    if not isinstance(index, pd.DatetimeIndex):
        index = pd.DatetimeIndex(index)
    if index.tz is not None:
        index = index.tz_convert("UTC").tz_localize(None)
    return index.normalize()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def validate_trading_day(
    market: str,
    d: _dt.date,
    *,
    align: _AlignMode = "error",
) -> _dt.date:
    """Validate that ``d`` is a trading day for ``market``.

    Parameters
    ----------
    market:
        Market code (see :mod:`stock_backtest.backtest.calendar`).
    d:
        Date to validate.
    align:
        - ``'error'`` (default): raise :class:`NonTradingDayError` if ``d`` is
          not a trading day.
        - ``'previous'``: return the nearest trading day on or before ``d``.
        - ``'next'``: return the nearest trading day on or after ``d``.

    Returns
    -------
    datetime.date
        ``d`` unchanged if it is already a trading day, otherwise the aligned
        trading day (for ``align != 'error'``).

    Raises
    ------
    NonTradingDayError
        If ``align='error'`` and ``d`` is not a trading day.
    ValueError
        If ``align`` is not one of the three accepted literals.
    """
    day = _to_date(d)
    if is_trading_day(market, day):
        return day

    if align == "error":
        raise NonTradingDayError(market, day)
    if align == "previous":
        return previous_trading_day(market, day)
    if align == "next":
        return next_trading_day(market, day)
    raise ValueError(
        f"Unknown align mode: {align!r}. Expected 'error', 'previous', or 'next'."
    )


def validate_date_range(
    market: str,
    start: _dt.date,
    end: _dt.date,
    prices_index: pd.DatetimeIndex,
    *,
    strict: bool = True,
) -> None:
    """Verify that ``prices_index`` covers every trading day in ``[start, end]``.

    Parameters
    ----------
    market:
        Market code.
    start, end:
        Inclusive bounds.
    prices_index:
        Index of available price rows. Will be normalised to tz-naive midnight.
    strict:
        - ``True`` (default): raise :class:`MissingPriceError` on the first
          missing trading day.
        - ``False``: emit a ``logging.warning`` listing missing days and
          return without raising.

    Raises
    ------
    MissingPriceError
        If ``strict`` is true and at least one trading day is missing.
    """
    start_d = _to_date(start)
    end_d = _to_date(end)

    expected = get_trading_days(market, start_d, end_d)
    available = _normalize_index(prices_index)

    missing = expected.difference(available)
    if len(missing) == 0:
        return

    first_missing: _dt.date = missing[0].date()
    sample = ", ".join(d.date().isoformat() for d in missing[:5])
    more = "" if len(missing) <= 5 else f" (+{len(missing) - 5} more)"
    msg = (
        f"Price index missing {len(missing)} trading day(s) for market "
        f"{market!r} in [{start_d}..{end_d}]: {sample}{more}"
    )

    if strict:
        raise MissingPriceError(None, first_missing, msg)
    _logger.warning(msg)


def align_to_trading_day(
    market: str,
    dates: pd.DatetimeIndex,
    *,
    direction: _Direction = "previous",
) -> pd.DatetimeIndex:
    """Vectorised alignment of ``dates`` to ``market`` trading days.

    Each entry of ``dates`` that is already a trading day is kept; non-trading
    days are snapped to the nearest trading day in ``direction``.

    For ``CRYPTO`` every day is a trading day, so the input is returned
    untouched (after normalisation).

    Parameters
    ----------
    market:
        Market code.
    dates:
        Input dates (may contain weekends/holidays, duplicates, or be
        unsorted; order is preserved).
    direction:
        - ``'previous'``: snap to the closest session on or before each date.
        - ``'next'``: snap to the closest session on or after each date.

    Returns
    -------
    pandas.DatetimeIndex
        Same length as ``dates``, tz-naive and normalised to midnight.

    Raises
    ------
    ValueError
        If ``direction`` is not ``'previous'`` or ``'next'``.
    """
    if direction not in ("previous", "next"):
        raise ValueError(
            f"Unknown direction: {direction!r}. Expected 'previous' or 'next'."
        )

    idx = _normalize_index(dates)
    if len(idx) == 0:
        return idx

    # Expand the session window slightly beyond the min/max so that snapping
    # near the boundaries still lands on a real session.
    pad = pd.Timedelta(days=14)
    session_start = (idx.min() - pad).date()
    session_end = (idx.max() + pad).date()
    sessions = get_trading_days(market, session_start, session_end)

    if len(sessions) == 0:
        # No sessions available (extremely narrow crypto-only fallback etc.)
        return idx

    # searchsorted gives us a vectorised nearest-boundary lookup.
    sessions_np = sessions.values.astype("datetime64[ns]")
    idx_np = idx.values.astype("datetime64[ns]")

    if direction == "previous":
        # For each date, find the rightmost session <= date.
        pos = np.searchsorted(sessions_np, idx_np, side="right") - 1
        pos = np.clip(pos, 0, len(sessions_np) - 1)
    else:  # next
        # Find the leftmost session >= date.
        pos = np.searchsorted(sessions_np, idx_np, side="left")
        pos = np.clip(pos, 0, len(sessions_np) - 1)

    return pd.DatetimeIndex(sessions_np[pos])


def assert_universe_coverage(
    market_by_asset: dict[int, str],
    prices: pd.DataFrame,
    start: _dt.date,
    end: _dt.date,
) -> None:
    """Assert that ``prices`` covers every trading day per asset's market.

    Parameters
    ----------
    market_by_asset:
        Mapping ``asset_id -> market_code``. Every column of ``prices`` must
        appear as a key; extra keys are ignored.
    prices:
        DataFrame with ``index = date`` and ``columns = asset_id``. Any NaN
        value counts as a missing observation (trading day present but no
        price).
    start, end:
        Inclusive bounds of the required coverage window.

    Raises
    ------
    MissingPriceError
        If one or more ``(asset_id, date)`` pairs are missing. The error
        message enumerates every offending asset so callers can fix the full
        set in one pass rather than chase one-at-a-time.
    """
    start_d = _to_date(start)
    end_d = _to_date(end)

    if prices.empty:
        if not market_by_asset:
            return
        # If we have assets declared but no prices at all, fail clearly.
        any_asset = next(iter(market_by_asset))
        raise MissingPriceError(
            any_asset,
            start_d,
            f"prices DataFrame is empty but {len(market_by_asset)} asset(s) "
            f"are declared in market_by_asset",
        )

    price_index = _normalize_index(prices.index)
    # Align the DataFrame's index to normalised form so NaN lookup works.
    normalized_prices = prices.copy()
    normalized_prices.index = price_index

    issues: list[
        tuple[int, str, _dt.date, int]
    ] = []  # (asset_id, market, first_missing, count)

    for asset_id in prices.columns:
        if asset_id not in market_by_asset:
            raise KeyError(
                f"asset_id={asset_id!r} present in prices.columns but missing "
                f"from market_by_asset"
            )
        market = market_by_asset[asset_id]
        expected = get_trading_days(market, start_d, end_d)
        if len(expected) == 0:
            continue

        series = normalized_prices[asset_id]
        # Dates that either don't appear at all, or appear with NaN.
        present = series.dropna().index
        missing = expected.difference(present)
        if len(missing) > 0:
            issues.append((int(asset_id), market, missing[0].date(), int(len(missing))))

    if not issues:
        return

    lines = [
        f"asset_id={aid} ({mkt}): first_missing={first.isoformat()} "
        f"missing_count={cnt}"
        for aid, mkt, first, cnt in issues
    ]
    msg = (
        f"Universe coverage failure for [{start_d}..{end_d}] on "
        f"{len(issues)} asset(s):\n  " + "\n  ".join(lines)
    )
    # Surface the first offender's asset_id / date in the exception attributes
    # while keeping the full list in the message.
    first_aid, _first_mkt, first_date, _first_cnt = issues[0]
    raise MissingPriceError(first_aid, first_date, msg)
