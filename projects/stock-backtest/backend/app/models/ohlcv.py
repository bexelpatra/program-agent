"""Ohlcv (일봉 시계열) ORM 모델.

TimescaleDB hypertable 로 운영. (asset_id, time) 복합 PK 로 동일 자산의 동일 시점 중복 차단.
close NOT NULL 강제 — 비거래일/공휴일에는 row 자체를 적재하지 않는 정책 (수집 레이어 책임).
adj_close 는 분할/배당 조정 후 종가 (yfinance Adj Close 매핑).
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Ohlcv(Base):
    """일봉 OHLCV 한 행.

    가격 컬럼은 Numeric(20, 8) — 암호화폐 소수점 8자리 수용 + 주식 정수 가격 모두 표현 가능.
    volume 은 Numeric(20, 0) — 정수형이지만 BigInteger 한계(2^63) 초과 가능성 대비 Numeric 사용.
    """

    __tablename__ = "ohlcv"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        primary_key=True,
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    open: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    high: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    low: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    # close NOT NULL — 비거래일 방어 정책 (architecture.md). 0/null close 는 수집 레이어에서 거부.
    close: Mapped[Decimal] = mapped_column(Numeric(20, 8), nullable=False)
    adj_close: Mapped[Decimal | None] = mapped_column(Numeric(20, 8), nullable=True)
    volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 0), nullable=True)
