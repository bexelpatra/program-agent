"""백테스트 결과 테이블 — runs / equity (hypertable) / trades / metrics.

Revision ID: 0003_backtest_tables
Revises: 0002_timeseries_tables
Create Date: 2026-04-29

architecture.md V3 § "DB 스키마" L242-251 (V1 살림) +
§ "비동기 job 모델" L437-446 (status/progress/cancel_requested) +
§ "에러 응답 계약" L450 (V2 살림 - error_json) 반영.

backtest_equity 는 TimescaleDB hypertable 로 변환. 0002 와 동일하게 try/except 로
일반 PostgreSQL 환경에서도 fail 하지 않도록 처리.

side CHECK ('BUY', 'SELL') 강제 — V3 § FX trade 미기록 정책 (architecture.md L389).
"""
import logging
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import DatabaseError

from alembic import op

logger = logging.getLogger("alembic.runtime.migration")

# revision identifiers, used by Alembic.
revision: str = "0003_backtest_tables"
down_revision: Union[str, Sequence[str], None] = "0002_timeseries_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create backtest_runs, backtest_equity (hypertable), backtest_trades, backtest_metrics."""
    op.create_table(
        "backtest_runs",
        sa.Column("run_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "user_id",
            sa.String(length=64),
            server_default=sa.text("'local'"),
            nullable=False,
        ),
        sa.Column("strategy_name", sa.String(length=64), nullable=False),
        sa.Column(
            "params",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "universe",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("base_currency", sa.String(length=8), nullable=False),
        sa.Column(
            "market_mode",
            sa.String(length=16),
            server_default=sa.text("'STOCK'"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=16),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column(
            "progress",
            sa.Float(),
            server_default=sa.text("0.0"),
            nullable=False,
        ),
        sa.Column(
            "cancel_requested",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "error_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("code_commit_hash", sa.String(length=64), nullable=True),
        sa.Column("data_hash", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index("ix_backtest_runs_status", "backtest_runs", ["status"])
    op.create_index(
        "ix_backtest_runs_run_hash",
        "backtest_runs",
        ["run_hash"],
        unique=True,
    )
    op.create_index(
        "ix_backtest_runs_created_at",
        "backtest_runs",
        ["created_at"],
    )

    op.create_table(
        "backtest_equity",
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("equity", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column("cash", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column(
            "drawdown",
            sa.Numeric(precision=10, scale=6),
            server_default=sa.text("0.0"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["backtest_runs.run_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("run_id", "time"),
    )

    op.create_table(
        "backtest_trades",
        sa.Column("trade_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("side", sa.String(length=8), nullable=False),
        sa.Column("qty", sa.Numeric(precision=20, scale=0), nullable=False),
        sa.Column("price", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.Column(
            "commission",
            sa.Numeric(precision=20, scale=8),
            server_default=sa.text("0"),
            nullable=False,
        ),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["backtest_runs.run_id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["assets.asset_id"],
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "side IN ('BUY', 'SELL')",
            name="ck_backtest_trades_side",
        ),
        sa.PrimaryKeyConstraint("trade_id"),
    )
    op.create_index(
        "ix_backtest_trades_run_time",
        "backtest_trades",
        ["run_id", "time"],
    )

    op.create_table(
        "backtest_metrics",
        sa.Column("metric_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("metric_name", sa.String(length=64), nullable=False),
        sa.Column("value", sa.Numeric(precision=20, scale=8), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["backtest_runs.run_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("metric_id"),
        sa.UniqueConstraint("run_id", "metric_name", name="uq_backtest_metrics_run_name"),
    )

    # TimescaleDB hypertable 변환 (0002 ohlcv 와 동일 패턴).
    # production 은 항상 TimescaleDB 가정이지만, CI/test 의 일반 PG 에서도 fail 하지 않도록
    # try/except 로 감싸고 실패 시 경고 로그만 남긴다.
    try:
        op.execute(
            "SELECT create_hypertable('backtest_equity', 'time', if_not_exists => TRUE)"
        )
    except DatabaseError as exc:
        logger.warning(
            "TimescaleDB hypertable 변환 실패 — 일반 PostgreSQL 환경으로 추정. "
            "backtest_equity 는 일반 테이블로 동작. 원인: %s",
            exc,
        )


def downgrade() -> None:
    """Drop backtest_metrics, backtest_trades, backtest_equity, backtest_runs (FK 순서 준수)."""
    op.drop_table("backtest_metrics")
    op.drop_index("ix_backtest_trades_run_time", table_name="backtest_trades")
    op.drop_table("backtest_trades")
    op.drop_table("backtest_equity")
    op.drop_index("ix_backtest_runs_created_at", table_name="backtest_runs")
    op.drop_index("ix_backtest_runs_run_hash", table_name="backtest_runs")
    op.drop_index("ix_backtest_runs_status", table_name="backtest_runs")
    op.drop_table("backtest_runs")
