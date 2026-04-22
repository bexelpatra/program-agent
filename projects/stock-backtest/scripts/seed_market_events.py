"""Seed script for :mod:`market_events` table.

Inserts the following event categories:

1. US presidential elections (1980, 1984, ..., 2024) — simplified to the
   **first Tuesday of November** of each year.
2. US midterm elections (1982, 1986, ..., 2022) — same date rule.
3. FOMC meeting dates:
   - 2021~2025: **hard-coded actual meeting dates** (approx. 8 per year).
   - Years outside this window: **approximation** — third Wednesday of
     Mar / Jun / Sep / Dec (quarterly center-week proxy).  This is an
     approximation only and should be refined for serious research.
4. Earnings-season peaks: **third Friday of Jan / Apr / Jul / Oct** as
   single-day marker events.
5. KR presidential elections: 2012, 2017, 2022 (actual dates).
6. KR general elections: 2012, 2016, 2020, 2024 (actual dates).

The ``market_events`` table has no UNIQUE constraint on
``(country, type, event_date)``.  The script therefore performs a
**SELECT-then-INSERT** dedup: existing rows matching the tuple are
skipped.  Re-running the script is idempotent.

Usage
-----
    python -m scripts.seed_market_events

or direct execution:

    python projects/stock-backtest/scripts/seed_market_events.py
"""
from __future__ import annotations

import calendar
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

# Allow running as a standalone script: ensure the package src/ is importable.
_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from sqlalchemy import select  # noqa: E402

from stock_backtest.data.db import get_session  # noqa: E402
from stock_backtest.data.models import MarketEvent  # noqa: E402


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------
def _first_weekday_of_month(year: int, month: int, weekday: int) -> date:
    """Return the first date in (year, month) whose ``weekday()`` matches.

    ``weekday``: Monday=0 ... Sunday=6.
    """
    for day in range(1, 8):
        d = date(year, month, day)
        if d.weekday() == weekday:
            return d
    raise AssertionError("unreachable")


def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """Return the n-th (1-based) occurrence of ``weekday`` in (year, month)."""
    first = _first_weekday_of_month(year, month, weekday)
    target_day = first.day + (n - 1) * 7
    last_day = calendar.monthrange(year, month)[1]
    if target_day > last_day:
        raise ValueError(
            f"No {n}-th weekday={weekday} in {year}-{month:02d}"
        )
    return date(year, month, target_day)


# ---------------------------------------------------------------------------
# Event builders
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class EventRow:
    country: str
    type: str
    event_date: date
    meta: dict


def _us_election_date(year: int) -> date:
    """First Tuesday of November (simplified)."""
    return _first_weekday_of_month(year, 11, weekday=1)  # Tue=1


def us_presidential_elections() -> list[EventRow]:
    years = list(range(1980, 2025, 4))  # 1980..2024 inclusive
    return [
        EventRow("US", "presidential_election", _us_election_date(y), {"year": y})
        for y in years
    ]


def us_midterm_elections() -> list[EventRow]:
    years = list(range(1982, 2023, 4))  # 1982..2022 inclusive (non-presidential even years)
    return [
        EventRow("US", "midterm_election", _us_election_date(y), {"year": y})
        for y in years
    ]


# Actual FOMC meeting dates (end-day of 2-day meetings), 2021-2025.
# Source: Federal Reserve FOMC calendars. 8 scheduled meetings per year.
_FOMC_ACTUAL: dict[int, list[date]] = {
    2021: [
        date(2021, 1, 27),
        date(2021, 3, 17),
        date(2021, 4, 28),
        date(2021, 6, 16),
        date(2021, 7, 28),
        date(2021, 9, 22),
        date(2021, 11, 3),
        date(2021, 12, 15),
    ],
    2022: [
        date(2022, 1, 26),
        date(2022, 3, 16),
        date(2022, 5, 4),
        date(2022, 6, 15),
        date(2022, 7, 27),
        date(2022, 9, 21),
        date(2022, 11, 2),
        date(2022, 12, 14),
    ],
    2023: [
        date(2023, 2, 1),
        date(2023, 3, 22),
        date(2023, 5, 3),
        date(2023, 6, 14),
        date(2023, 7, 26),
        date(2023, 9, 20),
        date(2023, 11, 1),
        date(2023, 12, 13),
    ],
    2024: [
        date(2024, 1, 31),
        date(2024, 3, 20),
        date(2024, 5, 1),
        date(2024, 6, 12),
        date(2024, 7, 31),
        date(2024, 9, 18),
        date(2024, 11, 7),
        date(2024, 12, 18),
    ],
    2025: [
        date(2025, 1, 29),
        date(2025, 3, 19),
        date(2025, 5, 7),
        date(2025, 6, 18),
        date(2025, 7, 30),
        date(2025, 9, 17),
        date(2025, 10, 29),
        date(2025, 12, 10),
    ],
}


def fomc_events() -> list[EventRow]:
    """FOMC events. 2021-2025 actual; other years approximated.

    Approximation: third Wednesday of Mar/Jun/Sep/Dec (4 per year) for
    years in [2000, 2020].  Marked in meta as ``{"approx": true}``.
    """
    out: list[EventRow] = []

    # Approximation for 2000..2020
    for year in range(2000, 2021):
        for month in (3, 6, 9, 12):
            d = _nth_weekday_of_month(year, month, weekday=2, n=3)  # Wed=2
            out.append(
                EventRow(
                    "US",
                    "fomc",
                    d,
                    {"approx": True, "year": year, "month": month},
                )
            )

    # Actual 2021..2025
    for year in sorted(_FOMC_ACTUAL):
        for d in _FOMC_ACTUAL[year]:
            out.append(EventRow("US", "fomc", d, {"approx": False, "year": year}))
    return out


def earnings_season_peaks() -> list[EventRow]:
    """Third Friday of Jan / Apr / Jul / Oct, 2000..2025."""
    out: list[EventRow] = []
    for year in range(2000, 2026):
        for month in (1, 4, 7, 10):
            d = _nth_weekday_of_month(year, month, weekday=4, n=3)  # Fri=4
            out.append(
                EventRow(
                    "US",
                    "earnings_season",
                    d,
                    {"year": year, "month": month, "approx": True},
                )
            )
    return out


def kr_presidential_elections() -> list[EventRow]:
    """Actual KR presidential election dates."""
    data = [
        (2012, date(2012, 12, 19)),
        (2017, date(2017, 5, 9)),
        (2022, date(2022, 3, 9)),
    ]
    return [
        EventRow("KR", "presidential_election", d, {"year": y}) for y, d in data
    ]


def kr_general_elections() -> list[EventRow]:
    """Actual KR general (National Assembly) election dates."""
    data = [
        (2012, date(2012, 4, 11)),
        (2016, date(2016, 4, 13)),
        (2020, date(2020, 4, 15)),
        (2024, date(2024, 4, 10)),
    ]
    return [EventRow("KR", "general_election", d, {"year": y}) for y, d in data]


# ---------------------------------------------------------------------------
# DB insertion
# ---------------------------------------------------------------------------
def _all_events() -> list[EventRow]:
    return (
        us_presidential_elections()
        + us_midterm_elections()
        + fomc_events()
        + earnings_season_peaks()
        + kr_presidential_elections()
        + kr_general_elections()
    )


def insert_events(events: Iterable[EventRow]) -> dict[str, int]:
    """Insert events with dedup (skip rows matching (country,type,event_date))."""
    events = list(events)
    inserted = 0
    skipped = 0
    with get_session() as session:
        # Preload existing (country,type,event_date) tuples into a set.
        existing_rows = session.execute(
            select(MarketEvent.country, MarketEvent.type, MarketEvent.event_date)
        ).all()
        existing = {(c, t, d) for c, t, d in existing_rows}

        for ev in events:
            key = (ev.country, ev.type, ev.event_date)
            if key in existing:
                skipped += 1
                continue
            session.add(
                MarketEvent(
                    country=ev.country,
                    type=ev.type,
                    event_date=ev.event_date,
                    meta=ev.meta,
                )
            )
            existing.add(key)
            inserted += 1
    return {"inserted": inserted, "skipped": skipped, "total": len(events)}


def summarize(events: list[EventRow]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in events:
        k = f"{e.country}:{e.type}"
        out[k] = out.get(k, 0) + 1
    return out


def main() -> None:
    events = _all_events()
    summary = summarize(events)
    print("Event counts (built):")
    for k, v in sorted(summary.items()):
        print(f"  {k:40s} {v:>4d}")
    print(f"  {'TOTAL':40s} {len(events):>4d}")

    result = insert_events(events)
    print("Insert result:", result)


if __name__ == "__main__":
    main()
