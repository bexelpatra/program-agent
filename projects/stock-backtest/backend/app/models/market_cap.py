"""AssetMarketCap — 자산 시가총액 시계열 ORM.

architecture.md V3 § "V3 Phase 2 — 신규 DB 테이블" 매핑.

Phase 2.2 에서 PykrxMarketCapSource cron 이 일별로 적재할 시계열 테이블.
Phase 2.1 (테마 정규화 차트) 에서는 빈 채로 두고, market_cap_weighting 호출 시
NotImplementedError 로 graceful 처리 — 테이블 자체는 0005 마이그레이션에서 미리 생성.

설계 노트:
- ``(asset_id, time)`` 복합 PK — 동일 자산 동일 시점 중복 차단.
- ohlcv 와 유사한 시계열이지만 ohlcv 보다 데이터량이 훨씬 작아 hypertable 변환은
  선택 사항 (alembic 에서 try/except 로 graceful).
- ``market_cap`` Numeric(24, 0) — KOSPI/NASDAQ 시총 (조 단위) 정수 표현 충분.
- ``shares_outstanding`` Numeric(20, 0) — 발행주식수 (없는 자산은 NULL).
- TimestampedModel mixin 미적용 — append-only 시계열, ``time`` 자체가 시점.
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class AssetMarketCap(Base):
    """자산 시가총액 한 시점 한 행.

    Phase 2.2 시가총액 가중치 (market_cap weighting) 계산의 기본 데이터.
    """

    __tablename__ = "asset_market_cap"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.asset_id", ondelete="CASCADE"),
        primary_key=True,
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    # 시가총액 (자산 currency 기준). KOSPI 대형주 / NASDAQ 메가캡 모두 수용.
    market_cap: Mapped[Decimal] = mapped_column(Numeric(24, 0), nullable=False)
    # 발행주식수. 일부 자산(ETF/지수) 은 NULL.
    shares_outstanding: Mapped[Decimal | None] = mapped_column(
        Numeric(20, 0),
        nullable=True,
    )
