"""Theme API Pydantic 스키마 (TASK-303 + TASK-305).

architecture.md V3 § "V3 Phase 2 — 테마주 추적/관찰 모듈" L823~ + § "API (Phase 2)"
L1023-1033 + § "정규화 차트 사양" L1038-1045 근거.

도메인 엔티티(`app.domain.themes.entity.{Theme,ThemeAsset,AssetThemeHistory}`) 와
1:1 매핑하지만, FastAPI 직렬화 경계에서 명시적 DTO 를 두어 ORM/도메인이 응답
스키마에 결합되지 않게 한다 (`schemas/asset.py` 패턴 동일).

스키마 목록:
    - ThemeRead    GET 단건/목록 항목 (member_count 옵션 포함).
    - ThemeCreate  POST 본문 (slug 자동 생성 허용).
    - ThemeUpdate  PATCH 본문 (부분 갱신).
    - ThemeDetail  GET 상세 (active_members 포함).
    - ThemeAssetRead   ThemeDetail.active_members 항목 / POST add 응답.
    - ThemeAssetAdd    POST /themes/{id}/assets 본문.
    - AssetThemeHistoryRead  GET /assets/{id}/theme_history 항목.
    - SeriesPoint, UniverseMeta, ThemeChartResponse,
      ThemeCompareItem, ThemeCompareResponse  (TASK-305 정규화 차트 API).
"""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# `period_adjustment.AdjustmentReason` Literal 재사용 (TASK-305 추가 지시).
# 본 스키마 모듈은 도메인 비의존이라는 일반 규칙이 있지만, 이 Literal 은 단순
# 문자열 값 (DB 컬럼/도메인 모두 동일 4 값) 이라 결합이 발생하지 않는다.
ChartAdjustmentReason = Literal[
    "universe_start_later",
    "universe_end_earlier",
    "no_data",
    "ok",
]

# `asset_theme_history.event_type` CHECK ('ADDED','REMOVED','RECLASSIFIED')
# 와 동기 (DB CHECK + domain Literal).
EventType = Literal["ADDED", "REMOVED", "RECLASSIFIED"]

# `asset_theme_history.source` 값 — USER 수동 / AUTO 자동 분류.
HistorySource = Literal["USER", "AUTO"]


class ThemeRead(BaseModel):
    """GET /api/themes (목록) + GET /api/themes/{id} (단건) 응답 본체.

    멤버 카운트는 목록에서만 채워지는 옵션 필드. 단건 상세는 ThemeDetail 사용.
    """

    model_config = ConfigDict(frozen=True)

    theme_id: int
    name: str
    slug: str
    description: str | None = None
    user_id: str
    created_at: datetime
    # 목록 응답 시 active 멤버 수를 함께 노출 (UI 4 — 테마 카탈로그 카드).
    member_count: int | None = None


class ThemeCreate(BaseModel):
    """POST /api/themes 본문.

    검증:
        - name 필수 (1~120 자) — DB 컬럼 폭과 일치.
        - slug optional. 미지정 시 라우터가 name 으로부터 자동 생성.
        - description 자유 길이 (DB Text 컬럼).
        - user_id 는 멀티 사용자 prep — 디폴트 'local'.
    """

    name: str = Field(..., min_length=1, max_length=120)
    slug: str | None = Field(default=None, max_length=120)
    description: str | None = None
    user_id: str = Field(default="local", min_length=1, max_length=64)


class ThemeUpdate(BaseModel):
    """PATCH /api/themes/{id} 본문 (부분 갱신).

    필드가 None 이면 갱신 스킵 (Repository 동작 동기). 빈 문자열은 명시적 빈 값
    으로 취급 (현재 description 만 의미 있음 — name 빈 문자열은 422 에서 차단).
    """

    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None


class ThemeAssetRead(BaseModel):
    """ThemeDetail.active_members 의 단일 항목 + POST add 응답.

    Service / Repository 가 server_default 로 added_at 을 채우므로 응답 시점에
    항상 값이 있다. removed_at 은 active 항목에서는 None.
    """

    model_config = ConfigDict(frozen=True)

    theme_id: int
    asset_id: int
    added_at: datetime
    removed_at: datetime | None = None
    note: str | None = None


class ThemeDetail(ThemeRead):
    """GET /api/themes/{id} 응답 — ThemeRead + active_members 멤버 리스트."""

    active_members: list[ThemeAssetRead] = Field(default_factory=list)


class ThemeAssetAdd(BaseModel):
    """POST /api/themes/{id}/assets 본문.

    검증:
        - asset_id 필수 (FK RESTRICT, 존재하지 않으면 422 또는 404 라우터 매핑).
        - note 는 자유 길이.
    """

    asset_id: int = Field(..., ge=1)
    note: str | None = None


class AssetThemeHistoryRead(BaseModel):
    """GET /api/assets/{asset_id}/theme_history 응답 항목.

    append-only — domain.entity.AssetThemeHistory 와 1:1 매핑.
    """

    model_config = ConfigDict(frozen=True)

    history_id: int
    asset_id: int
    theme_id: int
    event_type: EventType
    from_theme_id: int | None = None
    occurred_at: datetime
    source: HistorySource
    note: str | None = None


# ============================================================================
# TASK-305 — 정규화 차트 API 스키마
# ============================================================================
#
# architecture.md V3 § "정규화 차트 사양" (L1038-1045):
#   - rebase=100: 첫 유효 가격을 100 으로 정규화
#   - weighting='equal': 멤버 산술 평균 (디폴트). 'market_cap' 은 Phase 2.2
#   - 공통 기간: universe 시작일 교집합 자동 산출
#
# 시리즈 포맷 결정 (Coder):
#   value 는 Decimal (rebase=100 이라 ~소수점 6 자리 정밀도 필요 + frontend Zod
#   string 매칭). frontend recharts 는 number 변환 후 사용. Pydantic 직렬화 시
#   Decimal → string 으로 직렬화돼 JSON 정밀도 손실이 없다.


class SeriesPoint(BaseModel):
    """일자별 단일 데이터 포인트 (정규화 차트 한 점).

    time 은 base 캘린더의 거래일 (timestamp). value 는 rebase=100 정규화 값.
    """

    model_config = ConfigDict(frozen=True)

    time: datetime
    value: Decimal


class UniverseMeta(BaseModel):
    """universe 시작일 교집합 + 사용자 통지 메타.

    period_adjustment.PeriodAdjustment 의 응답측 투영. adjusted_start/end 는
    실제 차트가 그려진 구간이며, affected_assets 는 교집합 산출에 영향을 준
    asset_id 목록 (UI 토스트 입력).
    """

    model_config = ConfigDict(frozen=True)

    adjusted_start: date
    adjusted_end: date
    affected_assets: list[int] = Field(default_factory=list)
    reason: ChartAdjustmentReason
    message: str


class ThemeChartResponse(BaseModel):
    """GET /api/themes/{theme_id}/chart 응답.

    members 는 asset_id 키 dict — 각 자산의 rebase=100 시리즈.
    aggregate 는 weighting 적용 후 합산 시리즈. OHLCV 가 비어있는 자산은
    members 에서 키 자체가 빠지고 universe_meta.affected_assets 에 등재된다.
    """

    model_config = ConfigDict(frozen=True)

    members: dict[int, list[SeriesPoint]]
    aggregate: list[SeriesPoint]
    universe_meta: UniverseMeta


class ThemeCompareItem(BaseModel):
    """GET /api/themes/compare 응답의 한 테마 entry."""

    model_config = ConfigDict(frozen=True)

    name: str
    aggregate: list[SeriesPoint]


class ThemeCompareResponse(BaseModel):
    """GET /api/themes/compare 응답.

    themes 는 theme_id → ThemeCompareItem. universe_meta 는 전체 비교 대상
    자산 통합 교집합 (모든 테마의 합집합 universe 에 대해 한 번 산출).
    """

    model_config = ConfigDict(frozen=True)

    themes: dict[int, ThemeCompareItem]
    universe_meta: UniverseMeta
