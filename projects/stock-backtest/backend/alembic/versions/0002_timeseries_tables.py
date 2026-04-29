"""시계열 테이블 — ohlcv (hypertable) + fx_rates + corporate_actions.

Revision ID: 0002_timeseries_tables
Revises: 0001_v3_baseline
Create Date: 2026-04-29

V3 architecture.md § "DB 스키마" L227-234 (V1 살림) 반영.
ohlcv 는 TimescaleDB hypertable 로 변환. fx_rates 는 데이터량이 적어 일반 테이블.
corporate_actions 는 (asset_id, time) 인덱스로 시계열 조회 최적화.
"""
import logging
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import DatabaseError

from alembic import op

logger = logging.getLogger("alembic.runtime.migration")

# revision identifiers, used by Alembic.
revision: str = "0002_timeseries_tables"
down_revision: Union[str, Sequence[str], None] = "0001_v3_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create ohlcv (hypertable), fx_rates, corporate_actions."""
    op.create_table(
        "ohlcv",
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column("high", sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column("low", sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column("close", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column("adj_close", sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column("volume", sa.Numeric(precision=20, scale=0), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("asset_id", "time"),
    )

    op.create_table(
        "fx_rates",
        sa.Column("base_ccy", sa.String(length=8), nullable=False),
        sa.Column("quote_ccy", sa.String(length=8), nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("rate", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.PrimaryKeyConstraint("base_ccy", "quote_ccy", "time"),
    )

    op.create_table(
        "corporate_actions",
        sa.Column("action_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("value", sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column(
            "meta",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("action_id"),
    )
    op.create_index(
        "ix_corporate_actions_asset_time",
        "corporate_actions",
        ["asset_id", "time"],
    )

    # TimescaleDB hypertable 변환.
    # production 은 항상 TimescaleDB 가정이지만, CI/test 의 일반 PG 에서도 fail 하지 않도록
    # try/except 로 감싸고 실패 시 경고 로그만 남긴다.
    try:
        op.execute(
            "SELECT create_hypertable('ohlcv', 'time', if_not_exists => TRUE)"
        )
    except DatabaseError as exc:
        logger.warning(
            "TimescaleDB hypertable 변환 실패 — 일반 PostgreSQL 환경으로 추정. "
            "ohlcv 는 일반 테이블로 동작. 원인: %s",
            exc,
        )


def downgrade() -> None:
    """Drop corporate_actions, fx_rates, ohlcv (hypertable 자동 해제)."""
    op.drop_index(
        "ix_corporate_actions_asset_time",
        table_name="corporate_actions",
    )
    op.drop_table("corporate_actions")
    op.drop_table("fx_rates")
    op.drop_table("ohlcv")
