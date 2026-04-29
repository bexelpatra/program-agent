"""Alembic 마이그레이션 환경.

sqlalchemy.url 은 alembic.ini 에 빈 값으로 두고, 본 모듈에서
app.core.config 의 Settings.database_url 을 동적으로 주입한다.
이유: 환경변수(.env) 단일 소스 유지 + 운영/CI/로컬 분기 단순화.
"""
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# alembic 은 backend/ 에서 실행되지만, app.* 패키지 import 보장을 위해 path 강제 삽입.
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.core.config import get_settings  # noqa: E402
from app.core.db import Base  # noqa: E402

# app.models 의 모든 모델을 import 해 Base.metadata 가 채워지도록 한다.
# 현재 모듈은 비어 있으나 TASK-010 부터 모델이 추가되면 자동 인식된다.
import app.models  # noqa: F401,E402

config = context.config

# .env 의 DATABASE_URL 을 alembic 컨텍스트에 주입.
config.set_main_option("sqlalchemy.url", get_settings().database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """offline 모드: SQL script 만 출력. DB 연결 불필요."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """online 모드: 실제 Engine 으로 DB 연결 후 마이그레이션 적용."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
