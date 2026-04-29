"""CorporateAction (배당/분할/합병 등 권리 이벤트) ORM 모델.

action_id surrogate PK + (asset_id, time) 인덱스로 시계열 조회 최적화.
type 은 String + 애플리케이션 검증 — Postgres ENUM 마이그레이션 부담 회피 (assets.asset_type 과 동일 패턴).
value 의미는 type 별로 다름:
  - DIVIDEND: 1주당 배당금 (currency 는 자산의 currency 와 동일 가정)
  - SPLIT: 분할 비율 (예: 2:1 분할이면 2.0)
  - MERGER: 합병 비율
세부 정보는 meta JSONB 에 유연하게 적재.
"""
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CorporateAction(Base):
    """단일 권리 이벤트 한 건."""

    __tablename__ = "corporate_actions"
    __table_args__ = (
        Index("ix_corporate_actions_asset_time", "asset_id", "time"),
    )

    action_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        nullable=False,
    )
    # DIVIDEND / SPLIT / MERGER 등. Pydantic Literal 로 호출 경계에서 검증.
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    value: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    meta: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        server_default="{}",
    )
