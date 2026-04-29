"""FastAPI Depends 헬퍼.

라우터가 생성자 인자를 알 필요 없게 wiring 을 한 곳에 모은다.
- get_db: SessionLocal context — 라우터 종료 시점에 close 보장.
- get_asset_repo / get_ohlcv_repo: 세션을 받아 repository 생성. 라우터에서
  `Depends(get_db)` 로 받은 세션을 그대로 넘겨 단일 트랜잭션 boundary 를 유지한다.
"""
from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.data.asset_repository import SqlAssetRepository
from app.data.repositories.ohlcv_repository import OhlcvRepository


def get_db() -> Iterator[Session]:
    """FastAPI Depends 용 세션 제너레이터. 호출자가 commit/rollback 책임."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_asset_repo(session: Session) -> SqlAssetRepository:
    """라우터가 `Depends(get_db)` 로 받은 세션으로 repository 생성."""
    return SqlAssetRepository(session)


def get_ohlcv_repo(session: Session) -> OhlcvRepository:
    """라우터가 `Depends(get_db)` 로 받은 세션으로 repository 생성."""
    return OhlcvRepository(session)
