"""Seed the synthetic USD cash asset and its daily $1 OHLCV series.

The strategy form exposes "현금 대기" as a selectable asset; this is modeled
as a synthetic ticker:

- ``assets`` row: ``symbol='USD'``, ``market='CASH'``, ``asset_type='CASH'``,
  ``currency='USD'``, ``name='US Dollar Cash'``, ``start_date=2000-01-01``,
  ``active=True``.
- ``ohlcv`` rows: one per **calendar day** from 2000-01-01 through today,
  with ``open=high=low=close=adj_close=1.0`` and ``volume=0``.

Idempotency
-----------
- If the USD asset already exists, it is reused (no update).
- If OHLCV rows already exist, only days strictly newer than
  ``max(time)`` are appended.

Usage
-----
    python projects/stock-backtest/scripts/seed_usd_cash.py
    python -m scripts.seed_usd_cash         # from projects/stock-backtest
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# Ensure the package is importable when run as a standalone script.
_HERE = Path(__file__).resolve().parent
_SRC = _HERE.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from sqlalchemy.orm import Session  # noqa: E402

from stock_backtest.data.db import get_session  # noqa: E402
from stock_backtest.data.models import Asset  # noqa: E402
from stock_backtest.data.repository import (  # noqa: E402
    AssetRepository,
    OhlcvRepository,
)


SYMBOL = "USD"
MARKET = "CASH"
ASSET_TYPE = "CASH"
CURRENCY = "USD"
NAME = "US Dollar Cash"
START_DATE = date(2000, 1, 1)
BATCH_SIZE = 1000


def ensure_asset(session: Session) -> Asset:
    """Insert the USD cash asset if missing; return the persisted row."""
    repo = AssetRepository(session)
    existing = repo.get_by_symbol(SYMBOL, MARKET)
    if existing is not None:
        return existing
    asset = Asset(
        symbol=SYMBOL,
        market=MARKET,
        asset_type=ASSET_TYPE,
        name=NAME,
        currency=CURRENCY,
        active=True,
        start_date=START_DATE,
        meta={},
    )
    session.add(asset)
    session.flush()
    return asset


def _daily_rows(start: date, end: date) -> list[dict]:
    """Build ``[start, end]`` (inclusive) flat-$1 OHLCV rows."""
    rows: list[dict] = []
    cur = start
    one_day = timedelta(days=1)
    while cur <= end:
        ts = datetime(cur.year, cur.month, cur.day, tzinfo=timezone.utc)
        rows.append(
            {
                "time": ts,
                "open": 1.0,
                "high": 1.0,
                "low": 1.0,
                "close": 1.0,
                "adj_close": 1.0,
                "volume": 0.0,
            }
        )
        cur += one_day
    return rows


def seed_ohlcv(session: Session, asset_id: int, today: Optional[date] = None) -> int:
    """Append flat-$1 daily rows up to ``today`` (default: UTC today).

    Returns the number of rows inserted in this run (0 if already up to date).
    """
    if today is None:
        today = datetime.now(timezone.utc).date()

    repo = OhlcvRepository(session)
    last = repo.get_max_time(asset_id)
    if last is None:
        start = START_DATE
    else:
        start = last.date() + timedelta(days=1)

    if start > today:
        return 0

    rows = _daily_rows(start, today)
    inserted = 0
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        inserted += repo.upsert_bulk(asset_id, batch)
    return inserted


def main() -> None:
    """Entry point: ensure asset + OHLCV, print a one-line summary."""
    with get_session() as session:
        asset = ensure_asset(session)
        inserted = seed_ohlcv(session, asset.asset_id)
        print(
            f"USD cash seed: asset_id={asset.asset_id} "
            f"rows_inserted={inserted}"
        )


if __name__ == "__main__":
    main()
