"""v3 baseline — assets + ingestion_log.

Revision ID: 0001_v3_baseline
Revises:
Create Date: 2026-04-29

V3 시작 시점의 단일 baseline. V1/V2 의 11개 테이블은 폐기되었으며 본 마이그레이션은
빈 schema 가정. 기존 DB 가 V1/V2 잔재를 가지고 있다면 backend/alembic/README.md 의
"기존 DB 초기화" 절차를 먼저 수행할 것.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_v3_baseline"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create assets and ingestion_log tables."""
    op.create_table(
        "assets",
        sa.Column("asset_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("market", sa.String(length=16), nullable=False),
        sa.Column("asset_type", sa.String(length=32), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column(
            "meta",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=True,
        ),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("last_ingested_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("asset_id"),
        sa.UniqueConstraint("symbol", "market", name="uq_assets_symbol_market"),
    )
    op.create_index("ix_assets_market", "assets", ["market"])
    op.create_index("ix_assets_symbol", "assets", ["symbol"])
    op.create_index("ix_assets_active", "assets", ["active"])

    op.create_table(
        "ingestion_log",
        sa.Column("log_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("requested_start", sa.Date(), nullable=False),
        sa.Column("requested_end", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column(
            "rows_inserted",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "attempted_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("log_id"),
    )
    op.create_index("ix_ingestion_log_asset_id", "ingestion_log", ["asset_id"])


def downgrade() -> None:
    """Drop ingestion_log then assets (FK 순서 준수)."""
    op.drop_index("ix_ingestion_log_asset_id", table_name="ingestion_log")
    op.drop_table("ingestion_log")
    op.drop_index("ix_assets_active", table_name="assets")
    op.drop_index("ix_assets_symbol", table_name="assets")
    op.drop_index("ix_assets_market", table_name="assets")
    op.drop_table("assets")
