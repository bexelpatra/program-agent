"""Phase 2 — themes / theme_assets / asset_theme_history + asset_market_cap.

Revision ID: 0005_theme_tables
Revises: 0004_fractional_qty
Create Date: 2026-05-12

V3 architecture.md § "V3 Phase 2 — 테마주 추적/관찰 모듈" L823~ 의 도메인 모델
+ 신규 DB 테이블 매핑.

추가 테이블 4 개:
1. ``themes`` — 사용자 큐레이션 테마 헤더. (user_id, slug) UNIQUE.
2. ``theme_assets`` — 테마-자산 N:M. soft delete (``removed_at``) + 복합 PK
   ``(theme_id, asset_id, added_at)``. 활성 멤버 가속용 부분 인덱스
   ``ix_theme_assets_active``.
3. ``asset_theme_history`` — append-only ADDED/REMOVED/RECLASSIFIED 이벤트 로그.
   ``event_type`` CHECK 제약.
4. ``asset_market_cap`` — Phase 2.2 시가총액 시계열 (현 Phase 2.1 에서 선행
   적재). (asset_id, time) 복합 PK. hypertable 변환은 TimescaleDB 환경에서만
   (try/except graceful).

AssetType Literal 'STOCK' 추가:
- ``assets.asset_type`` 컬럼은 ``String(32)`` (NO ENUM, ``backend/app/models/asset.py:37``
  실측 + Reviewer r2 PASS) → DB DDL 변경 없음. Python/TS Literal 4곳 (entity.py /
  schemas/asset.py / data/seed/assets_catalog.py / frontend/lib/api/schemas.ts)
  만 동기.
"""
import logging
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.exc import DatabaseError

from alembic import op

logger = logging.getLogger("alembic.runtime.migration")

# revision identifiers, used by Alembic.
revision: str = "0005_theme_tables"
down_revision: Union[str, Sequence[str], None] = "0004_fractional_qty"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create themes, theme_assets, asset_theme_history, asset_market_cap."""
    # 1) themes — 테마 헤더.
    op.create_table(
        "themes",
        sa.Column("theme_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "user_id",
            sa.String(length=64),
            server_default=sa.text("'local'"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("theme_id"),
        sa.UniqueConstraint("user_id", "slug", name="uq_themes_user_slug"),
    )

    # 2) theme_assets — 테마-자산 매핑 (soft delete).
    op.create_table(
        "theme_assets",
        sa.Column("theme_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column(
            "added_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["theme_id"],
            ["themes.theme_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("theme_id", "asset_id", "added_at"),
    )
    # 활성 멤버 (removed_at IS NULL) 조회 가속 — 부분 인덱스.
    op.execute(
        "CREATE INDEX ix_theme_assets_active "
        "ON theme_assets (theme_id) "
        "WHERE removed_at IS NULL"
    )

    # 3) asset_theme_history — append-only 이벤트 로그.
    op.create_table(
        "asset_theme_history",
        sa.Column(
            "history_id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("theme_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=20), nullable=False),
        sa.Column("from_theme_id", sa.Integer(), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "source",
            sa.String(length=16),
            server_default=sa.text("'USER'"),
            nullable=False,
        ),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["theme_id"],
            ["themes.theme_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["from_theme_id"],
            ["themes.theme_id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("history_id"),
        sa.CheckConstraint(
            "event_type IN ('ADDED','REMOVED','RECLASSIFIED')",
            name="ck_asset_theme_history_event_type",
        ),
    )

    # 4) asset_market_cap — Phase 2.2 시계열 (선행 적재).
    op.create_table(
        "asset_market_cap",
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("market_cap", sa.Numeric(precision=24, scale=0), nullable=False),
        sa.Column(
            "shares_outstanding",
            sa.Numeric(precision=20, scale=0),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("asset_id", "time"),
    )

    # TimescaleDB hypertable 변환 (선택 사항).
    # production = TimescaleDB 가정이지만, CI/test 의 일반 PG 환경에서도 fail 하지
    # 않도록 try/except 로 감싼다 (패턴: 0002_timeseries_tables.py L87-96).
    try:
        op.execute(
            "SELECT create_hypertable('asset_market_cap', 'time', if_not_exists => TRUE)"
        )
    except DatabaseError as exc:
        logger.warning(
            "TimescaleDB hypertable 변환 실패 — 일반 PostgreSQL 환경으로 추정. "
            "asset_market_cap 는 일반 테이블로 동작. 원인: %s",
            exc,
        )


def downgrade() -> None:
    """Drop asset_market_cap, asset_theme_history, theme_assets, themes (FK 역순)."""
    op.drop_table("asset_market_cap")
    op.drop_table("asset_theme_history")
    op.execute("DROP INDEX IF EXISTS ix_theme_assets_active")
    op.drop_table("theme_assets")
    op.drop_table("themes")
