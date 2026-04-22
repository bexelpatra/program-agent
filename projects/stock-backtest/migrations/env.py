"""Alembic environment for stock-backtest.

Uses SQLAlchemy 2.0 style and loads DATABASE_URL from .env. Alembic CLI
honors the `-x db=test` argument to target the test DB (DATABASE_URL_TEST).
"""
from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# --- Load .env from project root -------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Resolve DB URL (main vs test via `-x db=test`) ------------------------
x_args = context.get_x_argument(as_dictionary=True)
target_db = x_args.get("db", "main")

if target_db == "test":
    db_url = os.environ.get("DATABASE_URL_TEST")
else:
    db_url = os.environ.get("DATABASE_URL")

if not db_url:
    raise RuntimeError(
        f"DATABASE_URL{'_TEST' if target_db == 'test' else ''} not set in environment / .env"
    )

config.set_main_option("sqlalchemy.url", db_url)

# No ORM metadata at this stage; ORM models arrive in TASK-004.
target_metadata = None


def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
