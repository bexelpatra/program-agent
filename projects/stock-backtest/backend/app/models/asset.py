"""Asset (자산 마스터) ORM 모델.

DB 풍부 / UI 단순 원칙: market 은 UI 노출용 분류, asset_type 은 내부 정밀 분류.
(symbol, market) UNIQUE — 동일 ticker 가 KR/US 양쪽에 존재할 수 있음(예: 한국 상장 SPY 추종 ETF 와 US SPY).
"""
from datetime import date, datetime
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.models._base import TimestampedModel


class Asset(TimestampedModel, Base):
    """카탈로그 등록된 단일 자산.

    meta JSONB 는 추후 kr_tax_class 등 미래 확장을 위해 비워둠 — 컬럼 추가 마이그레이션 회피 목적.
    """

    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("symbol", "market", name="uq_assets_symbol_market"),
        Index("ix_assets_market", "market"),
        Index("ix_assets_symbol", "symbol"),
        Index("ix_assets_active", "active"),
    )

    asset_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # yfinance/pykrx ticker. 길이 32 는 BRK.B / KODEX200 / BTC-USD 등 모두 수용.
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    # KR / US / CRYPTO — UI 가 직접 노출하는 시장 분류.
    market: Mapped[str] = mapped_column(String(16), nullable=False)
    # EQUITY_INDEX / ETF / BOND / COMMODITY / CRYPTO — 내부 분류, Phase 2 에서 UI 세분화 검토.
    asset_type: Mapped[str] = mapped_column(String(32), nullable=False)
    # ISO 4217 코드. 환전/배당 계산 기준.
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    # 한글 표시명 (예: "코덱스 200").
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    # 미래 확장(kr_tax_class 등). default {} 로 NOT NULL 제약 회피하면서 코드는 nullable 처리 단순화.
    meta: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
        server_default="{}",
    )
    # 카탈로그 노출 여부. 백필 실패/철회 시 false 로 숨김.
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    # 백필 후 갱신 — 가장 오래된 일봉 일자.
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # 마지막 일일 ingestion 시각. 스케줄러가 갱신.
    last_ingested_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
