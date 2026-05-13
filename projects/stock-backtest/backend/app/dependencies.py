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
from app.data.theme_repository import SqlAlchemyUnitOfWork, SqlThemeRepository


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


def get_theme_repo(session: Session) -> SqlThemeRepository:
    """Theme Repository (TASK-303). Service 는 ThemeRepository Protocol 만 의존하나,
    FastAPI Depends 경계에서는 구상 클래스를 생성해 반환한다 (의존성 역전은 service
    호출 시점에 Protocol 기준으로 dispatch — `app.domain.themes.service`).
    """
    return SqlThemeRepository(session)


def get_theme_uow(session: Session) -> SqlAlchemyUnitOfWork:
    """Theme service 의 트랜잭션 경계 — `get_theme_repo` 와 **동일 Session** 을
    주입해야 trans 일관성이 보장된다 (라우터가 `Depends(get_db)` 단일 세션을 두
    함수에 모두 넘김).
    """
    return SqlAlchemyUnitOfWork(session)
