"""자산 API Pydantic 스키마.

architecture.md V3 § "자산 도메인 모델" L514-555 + § "V2 API" L426-428 근거.
도메인 엔티티(`app.domain.asset.entity.Asset`) 와 1:1 매핑하지만, FastAPI 직렬화 경계에서
명시적 DTO 를 두어 ORM/도메인이 응답 스키마에 결합되지 않도록 한다.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# UI 노출 시장 분류. 도메인 Market literal 과 동일 값을 가져야 한다.
Market = Literal["KR", "US", "CRYPTO"]
# 내부 정밀 분류. 도메인 AssetType literal 과 동일.
# STOCK = Phase 2 테마주 트랙 (개별주) — 백엔드 domain entity 와 1:1 동기.
AssetType = Literal["EQUITY_INDEX", "ETF", "BOND", "COMMODITY", "CRYPTO", "STOCK"]


class AssetRead(BaseModel):
    """자산 단건 응답 / 검색 결과 항목."""

    model_config = ConfigDict(frozen=True)

    asset_id: int
    symbol: str
    market: Market
    asset_type: AssetType
    currency: str
    name: str
    meta: dict[str, Any] = Field(default_factory=dict)
    active: bool
    start_date: date | None = None
    last_ingested_at: datetime | None = None


class AssetCreate(BaseModel):
    """POST /api/assets 요청 본문. 사용자 자유 추가 워크플로우 입력.

    검증:
        - symbol/name/currency 길이 제한 (DB 컬럼 폭과 일치).
        - meta 는 비어있을 수 있음 — 미래 확장(kr_tax_class) 자리만 마련.
    """

    symbol: str = Field(..., min_length=1, max_length=32)
    market: Market
    asset_type: AssetType
    currency: str = Field(..., min_length=2, max_length=8)
    name: str = Field(..., min_length=1, max_length=128)
    meta: dict[str, Any] = Field(default_factory=dict)


class AssetSearchQuery(BaseModel):
    """GET /api/assets 의 쿼리 파라미터 (라우터에서 직접 unpack — 참고용)."""

    q: str | None = None
    market: Market | None = None
    asset_type: AssetType | None = None
    limit: int = Field(50, ge=1, le=200)
    offset: int = Field(0, ge=0)


class OhlcvPoint(BaseModel):
    """GET /api/assets/{asset_id}/ohlcv 응답 항목.

    Decimal → float 환산은 라우터가 책임 (Numeric 컬럼은 로컬 단일 사용자 기준
    float 정밀도로 충분, JSON 표현 단순화 우선).
    """

    model_config = ConfigDict(frozen=True)

    time: datetime
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float
    adj_close: float | None = None
    volume: float | None = None


class AssetCreateResponse(BaseModel):
    """POST /api/assets 응답. 등록된 자산 + 백필 큐잉 여부 + 한국어 안내."""

    model_config = ConfigDict(frozen=True)

    asset: AssetRead
    backfill_enqueued: bool
    note: str | None = None
