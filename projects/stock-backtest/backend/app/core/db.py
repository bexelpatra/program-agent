"""SQLAlchemy 2.0 Engine / SessionLocal / DeclarativeBase 정의.

비즈니스 로직 금지 — 본 모듈은 DB 연결 객체 정의와 FastAPI 의존성 주입 헬퍼만 제공한다.
"""
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

_settings = get_settings()

# pool_pre_ping 으로 끊어진 커넥션 자동 재시도 (Postgres idle timeout 방어).
engine = create_engine(
    _settings.database_url,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


class Base(DeclarativeBase):
    """모든 ORM 모델의 공통 베이스. metadata 단일화 위해 분리하지 않는다."""


def get_db() -> Iterator[Session]:
    """FastAPI Depends 용 세션 제너레이터. 호출자가 commit/rollback 책임."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
