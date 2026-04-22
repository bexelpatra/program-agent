"""add CASH market and asset_type to assets check constraints

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-14

Extends ``ck_assets_market`` and ``ck_assets_asset_type`` to allow the
synthetic ``USD`` cash asset (``market='CASH'``, ``asset_type='CASH'``)
required by the strategy form's "현금 대기" option (TASK-046).
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("ck_assets_market", "assets", type_="check")
    op.create_check_constraint(
        "ck_assets_market",
        "assets",
        "market IN ('KR','US','GLOBAL','CRYPTO','CASH')",
    )
    op.drop_constraint("ck_assets_asset_type", "assets", type_="check")
    op.create_check_constraint(
        "ck_assets_asset_type",
        "assets",
        "asset_type IN ('EQUITY_INDEX','ETF','BOND','COMMODITY','CRYPTO','CASH')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_assets_asset_type", "assets", type_="check")
    op.create_check_constraint(
        "ck_assets_asset_type",
        "assets",
        "asset_type IN ('EQUITY_INDEX','ETF','BOND','COMMODITY','CRYPTO')",
    )
    op.drop_constraint("ck_assets_market", "assets", type_="check")
    op.create_check_constraint(
        "ck_assets_market",
        "assets",
        "market IN ('KR','US','GLOBAL','CRYPTO')",
    )
