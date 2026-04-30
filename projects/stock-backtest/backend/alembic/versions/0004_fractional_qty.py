"""fractional qty for crypto market.

Revision ID: 0004_fractional_qty
Revises: 0003_backtest_tables
Create Date: 2026-04-29

V3 Q8 재결정 (architecture.md L609-615): 코인 한정 fractional 매매 허용.
backtest_trades.qty 컬럼을 Numeric(20, 0) → Numeric(20, 8) 로 변경.

배경:
- BTC 1코인 = $50k 같은 고가 자산이 작은 초기자본(예: $10k) 으로는 정수 단위
  매수 시 0개 체결 → equity 평탄선이 되어 모든 백테스트 결과가 망가짐.
- 사용자 첫 시도 사고(run_id=56) 에서 발견 후 정책 변경.
- 일반 주식의 fractional shares 는 실거래에서 일부 증권사만 지원하므로 V3 는
  CRYPTO 시장만 허용. 주식·ETF·지수·채권·원자재(KR/US)는 1주 단위 정수 유지.

호환성:
- 기존 정수 qty (예: 5) 는 Numeric(20, 8) 으로 변환 시에도 5.00000000 로 정확
  표현되어 손실 없음. downgrade 시 소수점 잔여가 있으면 절단(truncation) 가능 —
  CRYPTO 매매가 적재된 테이블의 downgrade 는 데이터 손실 위험.
"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004_fractional_qty"
down_revision: Union[str, Sequence[str], None] = "0003_backtest_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """backtest_trades.qty: Numeric(20, 0) → Numeric(20, 8)."""
    op.alter_column(
        "backtest_trades",
        "qty",
        existing_type=sa.Numeric(precision=20, scale=0),
        type_=sa.Numeric(precision=20, scale=8),
        existing_nullable=False,
    )


def downgrade() -> None:
    """backtest_trades.qty: Numeric(20, 8) → Numeric(20, 0).

    경고: CRYPTO 매매가 이미 적재되어 있으면 소수점이 절단되어 데이터 손실
    가능 (예: 0.19994 BTC → 0). 운영 환경에서는 백업 후 수행.
    """
    op.alter_column(
        "backtest_trades",
        "qty",
        existing_type=sa.Numeric(precision=20, scale=8),
        type_=sa.Numeric(precision=20, scale=0),
        existing_nullable=False,
    )
