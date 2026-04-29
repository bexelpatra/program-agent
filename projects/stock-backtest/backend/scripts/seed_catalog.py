"""자산 카탈로그 시드 적재 CLI.

`backend/app/data/seed/assets_catalog.py` 의 CATALOG 를 DB 의 assets 테이블에 멱등 UPSERT 한다.

사용:
    cd projects/stock-backtest/backend
    python -m scripts.seed_catalog

멱등성:
    (symbol, market) UNIQUE 제약을 충돌 키로 사용. 기존 행이 있으면 asset_type/currency/name/meta/active 만 갱신.
    start_date, last_ingested_at 은 백필러가 관리하므로 손대지 않는다.
"""
from __future__ import annotations

from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.db import SessionLocal
from app.data.seed.assets_catalog import CATALOG
from app.models import Asset


def seed() -> int:
    """카탈로그 전체를 UPSERT 후 행 수 반환."""
    with SessionLocal() as session:
        for row in CATALOG:
            stmt = pg_insert(Asset).values(**row).on_conflict_do_update(
                index_elements=["symbol", "market"],
                set_={
                    "asset_type": row["asset_type"],
                    "currency": row["currency"],
                    "name": row["name"],
                    "meta": row["meta"],
                    "active": True,
                },
            )
            session.execute(stmt)
        session.commit()
    return len(CATALOG)


if __name__ == "__main__":
    count = seed()
    print(f"Seeded {count} assets")
