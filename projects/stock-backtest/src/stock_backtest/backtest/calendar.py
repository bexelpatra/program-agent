"""Trading calendar utilities for KRX, NYSE, and 24/7 Crypto markets.

This module wraps :mod:`exchange_calendars` for equity markets and provides a
synthetic 365-day calendar for crypto assets. All returned timestamps are
**tz-naive** (UTC-normalised) ``pandas.Timestamp`` values so that downstream
code can mix them freely without timezone arithmetic.

Public API
----------
- :func:`get_trading_days` -- trading-day index for a single market.
- :func:`is_trading_day`   -- scalar trading-day check.
- :func:`previous_trading_day` / :func:`next_trading_day` -- align a date to
  the nearest trading day (inclusive of the given date when it is a trading
  day).
- :func:`common_trading_days` -- intersection of multiple markets' calendars
  (used for ``market_mode = MIXED``).
- :func:`union_trading_days`  -- union of multiple markets' calendars.

Market codes
------------
- ``KR`` / ``KRX`` / ``KOSPI`` / ``KOSDAQ`` -> ``XKRX``
- ``US`` / ``NYSE`` / ``NASDAQ``           -> ``XNYS``
- ``CRYPTO``                                -> synthetic 365-day calendar

Raises :class:`MarketNotSupportedError` for any other market code.
"""

from __future__ import annotations

import datetime as _dt
import functools
from typing import Iterable

import pandas as pd
import exchange_calendars as xcals


__all__ = [
    "MarketNotSupportedError",
    "get_trading_days",
    "is_trading_day",
    "previous_trading_day",
    "next_trading_day",
    "common_trading_days",
    "union_trading_days",
]


class MarketNotSupportedError(Exception):
    """Raised when a market code cannot be mapped to a known calendar."""


# Market code aliases -> canonical exchange_calendars code (or synthetic tag).
_MARKET_ALIASES: dict[str, str] = {
    # Korea
    "KR": "XKRX",
    "KRX": "XKRX",
    "KOSPI": "XKRX",
    "KOSDAQ": "XKRX",
    "XKRX": "XKRX",
    # United States
    "US": "XNYS",
    "NYSE": "XNYS",
    "NASDAQ": "XNYS",
    "XNYS": "XNYS",
    # Crypto (synthetic 365-day calendar)
    "CRYPTO": "CRYPTO",
}


def _resolve_market(market: str) -> str:
    """Return the canonical calendar code for ``market``.

    Parameters
    ----------
    market:
        Market identifier (case-insensitive).

    Raises
    ------
    MarketNotSupportedError
        If the market code is unknown.
    """
    if not isinstance(market, str) or not market:
        raise MarketNotSupportedError(f"Invalid market code: {market!r}")
    key = market.strip().upper()
    try:
        return _MARKET_ALIASES[key]
    except KeyError as exc:
        raise MarketNotSupportedError(
            f"Unsupported market code: {market!r}. "
            f"Supported: {sorted(set(_MARKET_ALIASES))}"
        ) from exc


@functools.lru_cache(maxsize=8)
def _get_calendar(code: str):
    """Module-level cached accessor for :class:`exchange_calendars.ExchangeCalendar`.

    ``CRYPTO`` is not a real exchange calendar; callers must handle it
    separately before reaching this function.
    """
    if code == "CRYPTO":
        raise ValueError("CRYPTO has no exchange_calendars object; handle separately")
    return xcals.get_calendar(code)


def _to_date(d: _dt.date | _dt.datetime | pd.Timestamp | str) -> _dt.date:
    """Coerce a value to a plain :class:`datetime.date`."""
    if isinstance(d, pd.Timestamp):
        return d.date()
    if isinstance(d, _dt.datetime):
        return d.date()
    if isinstance(d, _dt.date):
        return d
    # strings / anything else -> let pandas parse
    return pd.Timestamp(d).date()


def _normalize_index(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Return a tz-naive, normalised (midnight) ``DatetimeIndex``."""
    if index.tz is not None:
        index = index.tz_convert("UTC").tz_localize(None)
    return index.normalize()


def get_trading_days(
    market: str,
    start: _dt.date,
    end: _dt.date,
) -> pd.DatetimeIndex:
    """Return the trading-day index for ``market`` in ``[start, end]`` (inclusive).

    Parameters
    ----------
    market:
        Market code (see module docstring).
    start, end:
        Inclusive bounds (``datetime.date``).

    Returns
    -------
    pandas.DatetimeIndex
        Tz-naive, normalised to midnight. For ``CRYPTO`` this is every calendar
        day in the range; for equity markets it is the set of exchange sessions.
    """
    start_d = _to_date(start)
    end_d = _to_date(end)
    if end_d < start_d:
        return pd.DatetimeIndex([])

    code = _resolve_market(market)

    if code == "CRYPTO":
        return pd.date_range(start=start_d, end=end_d, freq="D", tz=None).normalize()

    cal = _get_calendar(code)
    # exchange_calendars >=4 uses `sessions_in_range` returning tz-naive index.
    sessions = cal.sessions_in_range(
        pd.Timestamp(start_d),
        pd.Timestamp(end_d),
    )
    return _normalize_index(pd.DatetimeIndex(sessions))


def is_trading_day(market: str, d: _dt.date) -> bool:
    """Return ``True`` if ``d`` is a trading day in ``market``."""
    day = _to_date(d)
    code = _resolve_market(market)
    if code == "CRYPTO":
        return True
    cal = _get_calendar(code)
    return bool(cal.is_session(pd.Timestamp(day)))


def previous_trading_day(market: str, d: _dt.date) -> _dt.date:
    """Return ``d`` if it is a trading day, otherwise the previous trading day.

    For ``CRYPTO`` this always returns ``d`` (every day is a trading day).
    """
    day = _to_date(d)
    code = _resolve_market(market)
    if code == "CRYPTO":
        return day
    cal = _get_calendar(code)
    ts = pd.Timestamp(day)
    # date_to_session with direction="previous" returns the session at or
    # before ``ts``. Falls back to manual search if library version differs.
    try:
        prev = cal.date_to_session(ts, direction="previous")
    except TypeError:  # pragma: no cover - older API
        if cal.is_session(ts):
            return day
        prev = cal.previous_session(ts)
    return _to_date(prev)


def next_trading_day(market: str, d: _dt.date) -> _dt.date:
    """Return ``d`` if it is a trading day, otherwise the next trading day.

    For ``CRYPTO`` this always returns ``d`` (every day is a trading day).
    """
    day = _to_date(d)
    code = _resolve_market(market)
    if code == "CRYPTO":
        return day
    cal = _get_calendar(code)
    ts = pd.Timestamp(day)
    try:
        nxt = cal.date_to_session(ts, direction="next")
    except TypeError:  # pragma: no cover - older API
        if cal.is_session(ts):
            return day
        nxt = cal.next_session(ts)
    return _to_date(nxt)


def _combine(
    markets: Iterable[str],
    start: _dt.date,
    end: _dt.date,
    how: str,
) -> pd.DatetimeIndex:
    markets = list(markets)
    if not markets:
        raise ValueError("markets must be a non-empty iterable")

    indices = [get_trading_days(m, start, end) for m in markets]
    result = indices[0]
    for idx in indices[1:]:
        if how == "intersection":
            result = result.intersection(idx)
        elif how == "union":
            result = result.union(idx)
        else:  # pragma: no cover - defensive
            raise ValueError(f"unknown combine op: {how}")
    return result.sort_values()


def common_trading_days(
    markets: list[str],
    start: _dt.date,
    end: _dt.date,
) -> pd.DatetimeIndex:
    """Return the **intersection** of trading days across ``markets``.

    Used by ``market_mode = MIXED`` to identify the shared session axis
    between e.g. KR and US equities.
    """
    return _combine(markets, start, end, how="intersection")


def union_trading_days(
    markets: list[str],
    start: _dt.date,
    end: _dt.date,
) -> pd.DatetimeIndex:
    """Return the **union** of trading days across ``markets`` (reference use)."""
    return _combine(markets, start, end, how="union")
