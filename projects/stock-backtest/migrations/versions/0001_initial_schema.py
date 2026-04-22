"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-14

Creates all base tables for stock-backtest:
- assets, corporate_actions, fx_rates, market_events, ingestion_log
- backtest_runs, backtest_trades, backtest_metrics
- ohlcv (Timescale hypertable, chunk = 1 year)
- backtest_equity (Timescale hypertable, chunk = 1 year)
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------------------------
# upgrade
# ---------------------------------------------------------------------------
def upgrade() -> None:
    # ---- assets ----------------------------------------------------------
    op.create_table(
        "assets",
        sa.Column("asset_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("symbol", sa.Text, nullable=False),
        sa.Column("market", sa.Text, nullable=False),
        sa.Column("asset_type", sa.Text, nullable=False),
        sa.Column("name", sa.Text),
        sa.Column("currency", sa.Text, nullable=False),
        sa.Column("active", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column("start_date", sa.Date),
        sa.Column("last_ingested_at", sa.TIMESTAMP(timezone=True)),
        sa.Column(
            "meta",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.UniqueConstraint("symbol", "market", name="uq_assets_symbol_market"),
        sa.CheckConstraint(
            "market IN ('KR','US','GLOBAL','CRYPTO')", name="ck_assets_market"
        ),
        sa.CheckConstraint(
            "asset_type IN ('EQUITY_INDEX','ETF','BOND','COMMODITY','CRYPTO')",
            name="ck_assets_asset_type",
        ),
    )
    op.execute(
        "COMMENT ON TABLE assets IS "
        "'Master list of tradable assets (indices, ETFs, bonds, commodities, crypto).'"
    )

    # ---- corporate_actions ----------------------------------------------
    op.create_table(
        "corporate_actions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "asset_id",
            sa.BigInteger,
            sa.ForeignKey("assets.asset_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("value", sa.Float),
        sa.Column(
            "meta",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.CheckConstraint(
            "type IN ('SPLIT','DIVIDEND')", name="ck_corporate_actions_type"
        ),
    )
    op.create_index(
        "ix_corporate_actions_asset_time",
        "corporate_actions",
        ["asset_id", "time"],
    )
    op.execute(
        "COMMENT ON TABLE corporate_actions IS "
        "'Per-asset splits and dividends (source-of-truth for adj_close recalc).'"
    )

    # ---- fx_rates --------------------------------------------------------
    op.create_table(
        "fx_rates",
        sa.Column("time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("base_ccy", sa.Text, nullable=False),
        sa.Column("quote_ccy", sa.Text, nullable=False),
        sa.Column("rate", sa.Float, nullable=False),
        sa.PrimaryKeyConstraint("base_ccy", "quote_ccy", "time", name="pk_fx_rates"),
    )
    op.create_index("ix_fx_rates_time", "fx_rates", ["time"])
    op.execute(
        "COMMENT ON TABLE fx_rates IS "
        "'Daily FX reference rates used to convert native-currency P&L to base_currency.'"
    )

    # ---- market_events ---------------------------------------------------
    op.create_table(
        "market_events",
        sa.Column("event_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("country", sa.Text, nullable=False),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("event_date", sa.Date, nullable=False),
        sa.Column(
            "meta",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.create_index(
        "ix_market_events_country_date", "market_events", ["country", "event_date"]
    )
    op.create_index("ix_market_events_type", "market_events", ["type"])
    op.execute(
        "COMMENT ON TABLE market_events IS "
        "'Political/economic events for seasonality analysis (elections, FOMC, earnings).'"
    )

    # ---- ingestion_log ---------------------------------------------------
    op.create_table(
        "ingestion_log",
        sa.Column("log_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "asset_id",
            sa.BigInteger,
            sa.ForeignKey("assets.asset_id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("requested_start", sa.Date),
        sa.Column("requested_end", sa.Date),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column(
            "rows_inserted", sa.Integer, nullable=False, server_default=sa.text("0")
        ),
        sa.Column("error_message", sa.Text),
        sa.Column(
            "attempted_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "status IN ('SUCCESS','FAILED','PARTIAL','REJECTED')",
            name="ck_ingestion_log_status",
        ),
    )
    op.create_index(
        "ix_ingestion_log_asset_attempted",
        "ingestion_log",
        ["asset_id", sa.text("attempted_at DESC")],
    )
    op.create_index("ix_ingestion_log_status", "ingestion_log", ["status"])
    op.execute(
        "COMMENT ON TABLE ingestion_log IS "
        "'Per-run ingestion audit log (success / partial / failed / rejected-nontrading-day).'"
    )

    # ---- backtest_runs ---------------------------------------------------
    op.create_table(
        "backtest_runs",
        sa.Column("run_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("run_hash", sa.Text, nullable=False, unique=True),
        sa.Column(
            "user_id", sa.Text, nullable=False, server_default=sa.text("'local'")
        ),
        sa.Column("strategy_name", sa.Text, nullable=False),
        sa.Column(
            "params",
            postgresql.JSONB,
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("universe", postgresql.JSONB, nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("base_currency", sa.Text, nullable=False),
        sa.Column("market_mode", sa.Text, nullable=False),
        sa.Column("code_commit_hash", sa.Text),
        sa.Column("data_hash", sa.Text),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "market_mode IN ('STOCK','CRYPTO','MIXED')",
            name="ck_backtest_runs_market_mode",
        ),
    )
    op.create_index(
        "ix_backtest_runs_user_created",
        "backtest_runs",
        ["user_id", sa.text("created_at DESC")],
    )
    op.create_index(
        "ix_backtest_runs_strategy", "backtest_runs", ["strategy_name"]
    )
    op.execute(
        "COMMENT ON TABLE backtest_runs IS "
        "'One row per backtest execution; run_hash enables result caching.'"
    )

    # ---- backtest_trades -------------------------------------------------
    op.create_table(
        "backtest_trades",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "run_id",
            sa.BigInteger,
            sa.ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "asset_id",
            sa.BigInteger,
            sa.ForeignKey("assets.asset_id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("side", sa.Text, nullable=False),
        sa.Column("qty", sa.Float, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column(
            "commission", sa.Float, nullable=False, server_default=sa.text("0")
        ),
        sa.Column("currency", sa.Text, nullable=False),
        sa.CheckConstraint(
            "side IN ('BUY','SELL')", name="ck_backtest_trades_side"
        ),
    )
    op.create_index(
        "ix_backtest_trades_run_time", "backtest_trades", ["run_id", "time"]
    )
    op.execute(
        "COMMENT ON TABLE backtest_trades IS "
        "'Executed trades emitted by the backtest engine for each run.'"
    )

    # ---- backtest_metrics ------------------------------------------------
    op.create_table(
        "backtest_metrics",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "run_id",
            sa.BigInteger,
            sa.ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("metric_name", sa.Text, nullable=False),
        sa.Column("value", sa.Float, nullable=False),
        sa.UniqueConstraint(
            "run_id", "metric_name", name="uq_backtest_metrics_run_metric"
        ),
    )
    op.execute(
        "COMMENT ON TABLE backtest_metrics IS "
        "'Per-run performance metrics (CAGR, Sharpe, MDD, ...).'"
    )

    # ---- ohlcv (hypertable) ---------------------------------------------
    op.create_table(
        "ohlcv",
        sa.Column("time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column(
            "asset_id",
            sa.BigInteger,
            sa.ForeignKey("assets.asset_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("open", sa.Float),
        sa.Column("high", sa.Float),
        sa.Column("low", sa.Float),
        sa.Column("close", sa.Float),
        sa.Column("adj_close", sa.Float),
        sa.Column("volume", sa.Float),
        sa.PrimaryKeyConstraint("asset_id", "time", name="pk_ohlcv"),
    )
    op.execute(
        "SELECT create_hypertable('ohlcv', 'time', "
        "chunk_time_interval => INTERVAL '1 year');"
    )
    op.execute(
        "COMMENT ON TABLE ohlcv IS "
        "'Daily OHLCV time series (Timescale hypertable, chunk=1 year, PK=(asset_id,time)).'"
    )

    # ---- backtest_equity (hypertable) -----------------------------------
    op.create_table(
        "backtest_equity",
        sa.Column(
            "run_id",
            sa.BigInteger,
            sa.ForeignKey("backtest_runs.run_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("equity", sa.Float, nullable=False),
        sa.Column("cash", sa.Float, nullable=False),
        sa.Column("drawdown", sa.Float),
        sa.PrimaryKeyConstraint("run_id", "time", name="pk_backtest_equity"),
    )
    op.execute(
        "SELECT create_hypertable('backtest_equity', 'time', "
        "chunk_time_interval => INTERVAL '1 year');"
    )
    op.execute(
        "COMMENT ON TABLE backtest_equity IS "
        "'Per-run daily equity curve (Timescale hypertable, chunk=1 year).'"
    )


# ---------------------------------------------------------------------------
# downgrade (reverse order)
# ---------------------------------------------------------------------------
def downgrade() -> None:
    op.drop_table("backtest_equity")
    op.drop_table("ohlcv")
    op.drop_table("backtest_metrics")
    op.drop_index("ix_backtest_trades_run_time", table_name="backtest_trades")
    op.drop_table("backtest_trades")
    op.drop_index("ix_backtest_runs_strategy", table_name="backtest_runs")
    op.drop_index("ix_backtest_runs_user_created", table_name="backtest_runs")
    op.drop_table("backtest_runs")
    op.drop_index("ix_ingestion_log_status", table_name="ingestion_log")
    op.drop_index("ix_ingestion_log_asset_attempted", table_name="ingestion_log")
    op.drop_table("ingestion_log")
    op.drop_index("ix_market_events_type", table_name="market_events")
    op.drop_index("ix_market_events_country_date", table_name="market_events")
    op.drop_table("market_events")
    op.drop_index("ix_fx_rates_time", table_name="fx_rates")
    op.drop_table("fx_rates")
    op.drop_index(
        "ix_corporate_actions_asset_time", table_name="corporate_actions"
    )
    op.drop_table("corporate_actions")
    op.drop_table("assets")
