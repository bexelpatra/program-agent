"""FxRate (환율 시계열) ORM 모델.

(base_ccy, quote_ccy, time) 복합 PK — 동일 통화쌍의 동일 시점 중복 차단.
일반 테이블 (hypertable 변환 안 함) — fx 데이터 양이 ohlcv 대비 작음 (architecture.md).
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class FxRate(Base):
    """단일 통화쌍의 한 시점 환율.

    base_ccy → quote_ccy 변환 비율. 예: USDKRW=1300 이면 base=USD, quote=KRW, rate=1300.
    """

    __tablename__ = "fx_rates"

    base_ccy: Mapped[str] = mapped_column(String(8), primary_key=True)
    quote_ccy: Mapped[str] = mapped_column(String(8), primary_key=True)
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    rate: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
