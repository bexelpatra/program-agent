"""add FX trade support to backtest_trades

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-14

Extends ``backtest_trades`` so that cross-currency conversions executed by
``Portfolio._ensure_cash`` can be recorded as first-class trade rows:

- ``side`` CHECK constraint accepts ``'FX'`` in addition to ``'BUY'``/``'SELL'``.
- ``asset_id`` FK becomes nullable (FX rows have no asset).
- New nullable columns: ``currency_from``, ``currency_to``, ``fx_rate``,
  ``spread_bps``.

Existing BUY/SELL rows remain fully compatible; all new columns are NULL for
them. See architecture.md section "FX TradeRecord 스키마 확장" for the design.
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- 1. Widen side CHECK to include FX --------------------------------
    op.drop_constraint(
        "ck_backtest_trades_side", "backtest_trades", type_="check"
    )
    op.create_check_constraint(
        "ck_backtest_trades_side",
        "backtest_trades",
        "side IN ('BUY','SELL','FX')",
    )

    # --- 2. Make asset_id nullable (FX rows have no asset) ----------------
    op.alter_column(
        "backtest_trades",
        "asset_id",
        existing_type=sa.BigInteger(),
        nullable=True,
    )

    # --- 3. New nullable FX metadata columns ------------------------------
    op.add_column(
        "backtest_trades",
        sa.Column("currency_from", sa.String(length=8), nullable=True),
    )
    op.add_column(
        "backtest_trades",
        sa.Column("currency_to", sa.String(length=8), nullable=True),
    )
    op.add_column(
        "backtest_trades",
        sa.Column("fx_rate", sa.Numeric(20, 10), nullable=True),
    )
    op.add_column(
        "backtest_trades",
        sa.Column("spread_bps", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    # Drop FX-only columns first.
    op.drop_column("backtest_trades", "spread_bps")
    op.drop_column("backtest_trades", "fx_rate")
    op.drop_column("backtest_trades", "currency_to")
    op.drop_column("backtest_trades", "currency_from")

    # Restore asset_id NOT NULL. Any FX rows must be purged first so the
    # ALTER doesn't fail on NULL values.
    op.execute("DELETE FROM backtest_trades WHERE side = 'FX' OR asset_id IS NULL")
    op.alter_column(
        "backtest_trades",
        "asset_id",
        existing_type=sa.BigInteger(),
        nullable=False,
    )

    # Restore narrower side CHECK.
    op.drop_constraint(
        "ck_backtest_trades_side", "backtest_trades", type_="check"
    )
    op.create_check_constraint(
        "ck_backtest_trades_side",
        "backtest_trades",
        "side IN ('BUY','SELL')",
    )
