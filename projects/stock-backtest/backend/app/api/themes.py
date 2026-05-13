"""테마 API 라우터 (TASK-303 + TASK-305 — Phase 2 테마주 추적/관찰 모듈).

architecture.md V3 § "V3 Phase 2 — 테마주 추적/관찰 모듈" § "API (Phase 2)"
L1023-1033 + § "정규화 차트 사양" L1038-1045 근거. 본 라우터는 9 endpoint 를
노출 (assets 라우터의 theme_history 1 endpoint 와 합쳐 Phase 2.1 backend
endpoint = 10).

엔드포인트:
    1. GET    /api/themes                                — 사용자 테마 목록 (멤버 카운트 포함, paginated).
    2. POST   /api/themes                                — 테마 생성 (slug 자동 생성).
    3. GET    /api/themes/{theme_id}                     — 테마 상세 (활성 멤버 list 포함).
    4. PATCH  /api/themes/{theme_id}                     — name/description 부분 갱신.
    5. DELETE /api/themes/{theme_id}                     — soft delete (활성 멤버 일괄 종료).
    6. POST   /api/themes/{theme_id}/assets              — 자산 추가 (history 자동 append).
    7. DELETE /api/themes/{theme_id}/assets/{asset_id}   — 자산 제거 (soft, history 자동 append).
    8. GET    /api/themes/{theme_id}/chart               — 정규화 차트 (rebase=100, members + aggregate).  (TASK-305)
    9. GET    /api/themes/compare                        — 다중 테마 정규화 비교 (aggregate only).         (TASK-305)

라우팅 우선순위 (TASK-305 결정):
    FastAPI 는 path 등록 순서로 매칭하므로 ``/compare`` 는 ``/{theme_id}`` 패턴
    보다 먼저 정의되어야 한다 (그렇지 않으면 ``compare`` 가 theme_id 로 잡혀
    422 ParseError 가 난다). 본 모듈에서는 chart/compare 가 별도 경로 segment
    (``/{id}/chart``, ``/compare``) 라 충돌이 없지만, compare 라우트 정의 시점은
    그대로 ``/{id}`` 와 분리해 둔다.

도메인 격리 (architecture.md L1063-1067 + TASK-309):
    본 라우터는 `app.domain.themes.*` 만 import. `app.domain.{engine, strategy,
    allocators, filters, trade, portfolio}` 는 **절대 import 하지 않는다** —
    Theme 트랙은 백테스팅 트랙과 양방향 격리. `app.domain.asset.period_adjustment`
    및 `app.domain.calendar` 는 백테스트 도메인이 아니라 자산/캘린더 공용
    인프라이므로 import 허용 (TASK-309 검증 대상은 engine/strategy/allocators/
    filters/trade/portfolio 6개에 한정 — 본 라우터에서 import 0 hit).

에러 매핑 (코더 가이드 § 8 "오류 처리 — 경계에서만"):
    - 404: 없는 theme_id / 없는 active asset / 없는 asset_id.
    - 409: 중복 slug (IntegrityError), 중복 active 멤버 (DuplicateActiveMember).
    - 422: validation 오류 (FastAPI 자동) + slug 자동 생성 실패
           + weighting=market_cap (Phase 2.2 미구현)
           + universe 가 비어 있거나 가용 OHLCV 0 (차트 의미 없음).
"""
from __future__ import annotations

import logging
import re
from datetime import date, datetime, time, timezone
from decimal import Decimal
from typing import Iterable, cast

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.health import COMMON_ERROR_RESPONSES
from app.dependencies import get_db, get_theme_repo, get_theme_uow
from app.domain.asset.entity import Asset as AssetEntity
from app.domain.asset.entity import AssetType, Market, Universe
from app.domain.asset.period_adjustment import adjust_period_for_universe
from app.domain.themes.entity import AssetThemeHistory as AssetThemeHistoryEntity
from app.domain.themes.entity import Theme as ThemeEntity
from app.domain.themes.entity import ThemeAsset as ThemeAssetEntity
from app.domain.themes.normalization import (
    compute_theme_aggregate,
    rebase_multi_series,
)
from app.domain.themes.service import (
    DuplicateActiveMember,
    InactiveMember,
    add_asset_to_theme,
    remove_asset_from_theme,
)
from app.models.asset import Asset as AssetModel
from app.models.ohlcv import Ohlcv as OhlcvModel
from app.schemas.common import ErrorResponse, PaginatedResponse
from app.schemas.theme import (
    AssetThemeHistoryRead,
    SeriesPoint,
    ThemeAssetAdd,
    ThemeAssetRead,
    ThemeChartResponse,
    ThemeCompareItem,
    ThemeCompareResponse,
    ThemeCreate,
    ThemeDetail,
    ThemeRead,
    ThemeUpdate,
    UniverseMeta,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/themes", tags=["themes"])

# COMMON_ERROR_RESPONSES (400/422/500) 외에 본 라우터가 사용하는 추가 코드 (404/409)
# 를 OpenAPI 에 명시 — schemathesis fuzz 가 "Undocumented HTTP status code" 로
# fail 하지 않도록 한다.
_NOT_FOUND_RESPONSES: dict[int | str, dict] = {
    **COMMON_ERROR_RESPONSES,
    404: {"model": ErrorResponse, "description": "리소스 없음"},
}
_NOT_FOUND_OR_CONFLICT_RESPONSES: dict[int | str, dict] = {
    **COMMON_ERROR_RESPONSES,
    404: {"model": ErrorResponse, "description": "리소스 없음"},
    409: {"model": ErrorResponse, "description": "충돌 (중복 slug 등)"},
}


# --- 변환 헬퍼 / slug 생성 -------------------------------------------------


def _theme_to_read(
    theme: ThemeEntity, member_count: int | None = None
) -> ThemeRead:
    """도메인 Theme → ThemeRead. member_count 는 목록에서만 채움."""
    return ThemeRead(
        theme_id=theme.theme_id,
        name=theme.name,
        slug=theme.slug,
        description=theme.description,
        user_id=theme.user_id,
        created_at=theme.created_at,
        member_count=member_count,
    )


def _theme_asset_to_read(member: ThemeAssetEntity) -> ThemeAssetRead:
    """도메인 ThemeAsset → ThemeAssetRead."""
    return ThemeAssetRead(
        theme_id=member.theme_id,
        asset_id=member.asset_id,
        added_at=member.added_at,
        removed_at=member.removed_at,
        note=member.note,
    )


def _history_to_read(h: AssetThemeHistoryEntity) -> AssetThemeHistoryRead:
    """도메인 AssetThemeHistory → AssetThemeHistoryRead."""
    return AssetThemeHistoryRead(
        history_id=h.history_id,
        asset_id=h.asset_id,
        theme_id=h.theme_id,
        event_type=h.event_type,
        from_theme_id=h.from_theme_id,
        occurred_at=h.occurred_at,
        source=h.source,
        note=h.note,
    )


# slug 자동 생성 — name 의 알파벳/숫자/한글 외 문자를 '-' 로 치환 후 120자 제한.
# `\w` 는 re.UNICODE 모드에서 한글을 포함. 빈 결과는 422 로 차단.
_SLUG_NON_WORD = re.compile(r"[^\w-]+", flags=re.UNICODE)
_SLUG_DASH_RUN = re.compile(r"-{2,}")


def _generate_slug(name: str) -> str:
    r"""name → slug 자동 변환.

    절차:
        1. 소문자 변환 (영문에만 영향, 한글은 동일).
        2. ``\w-`` 외 문자 → '-'.
        3. 연속 '-' 합치기 + 양끝 '-' 제거.
        4. 길이 120 자 클램프.
        5. 빈 문자열이면 빈 문자열 반환 (라우터가 422 결정).
    """
    candidate = _SLUG_NON_WORD.sub("-", name.lower())
    candidate = _SLUG_DASH_RUN.sub("-", candidate).strip("-")
    return candidate[:120]


# --- 1. GET /api/themes ----------------------------------------------------


@router.get(
    "",
    response_model=PaginatedResponse[ThemeRead],
    summary="테마 목록 (활성 멤버 카운트 포함)",
    responses=COMMON_ERROR_RESPONSES,
)
def list_themes(
    user_id: str = Query("local", min_length=1, max_length=64),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
) -> PaginatedResponse[ThemeRead]:
    """``user_id`` 의 모든 테마. Repository.list_themes 는 이미 정렬 + soft-delete
    제외. 본 라우터는 in-memory slice + 활성 멤버 카운트를 각 테마별로 조회한다.

    페이지네이션 모집단은 list_themes 의 전체 결과 길이 (현 alembic 0005 스키마에
    deleted_at 컬럼이 없어 별도 count 쿼리 불필요 — DB 호출 1회 + 멤버 카운트는
    limit 만큼만 추가).
    """
    repo = get_theme_repo(session)
    all_themes = repo.list_themes(user_id=user_id)
    total = len(all_themes)
    sliced = all_themes[offset : offset + limit]

    # 각 테마의 활성 멤버 수 조회. 향후 N+1 가 문제되면 단일 쿼리로 일괄 집계 가능
    # (현재는 limit<=200 + 테마당 1 쿼리 = 화면 4 카탈로그 카드 용도로 충분).
    items: list[ThemeRead] = []
    for t in sliced:
        active = repo.list_active_assets(t.theme_id)
        items.append(_theme_to_read(t, member_count=len(active)))

    page = (offset // limit) + 1 if limit > 0 else 1
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=limit,
    )


# --- 2. POST /api/themes ---------------------------------------------------


@router.post(
    "",
    response_model=ThemeRead,
    status_code=201,
    summary="테마 생성 (slug 미지정 시 자동 생성)",
    responses=_NOT_FOUND_OR_CONFLICT_RESPONSES,
)
def create_theme(
    payload: ThemeCreate,
    session: Session = Depends(get_db),
) -> ThemeRead:
    """POST /api/themes.

    HTTP 매핑:
        - 201: 생성 성공.
        - 409: (user_id, slug) UNIQUE 충돌 (IntegrityError).
        - 422: slug 자동 생성 실패 (예: name 이 모두 공백/특수문자).
    """
    repo = get_theme_repo(session)

    # slug 결정 — payload.slug 가 비어있으면 name 으로부터 자동 생성.
    raw_slug = payload.slug if payload.slug else _generate_slug(payload.name)
    if not raw_slug:
        raise HTTPException(
            status_code=422,
            detail=(
                f"slug 자동 생성 실패: 이름 '{payload.name}' 으로부터 유효한 slug 를 "
                "생성할 수 없습니다. slug 를 직접 지정하세요."
            ),
        )

    try:
        created = repo.create_theme(
            name=payload.name,
            slug=raw_slug,
            description=payload.description,
            user_id=payload.user_id,
        )
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"이미 존재하는 slug 입니다: user_id={payload.user_id} slug={raw_slug}",
        ) from exc

    return _theme_to_read(created)


# --- 2b. GET /api/themes/compare -------------------------------------------
#
# 라우팅 우선순위 정책 (FastAPI/starlette router 등록 순서 기반):
#   `/{theme_id}` 동적 path 가 `compare` 를 정수 theme_id 로 파싱하려다 422
#   RequestValidationError 를 발생시키는 것을 막기 위해, 정적 path 인
#   `/compare` 라우트를 `/{theme_id}` 라우트 등록보다 먼저 정의한다.
#   본 함수 본문에서 호출하는 `_compute_theme_chart` 헬퍼 / 응답 스키마는
#   파일 하단에 정의되어 있지만, 모듈 로드가 끝나는 시점에 모두 바인딩되므로
#   런타임 호출에는 문제가 없다.


@router.get(
    "/compare",
    response_model=ThemeCompareResponse,
    summary="다중 테마 정규화 비교 (aggregate only)",
    responses={
        **COMMON_ERROR_RESPONSES,
        404: {"model": ErrorResponse, "description": "리소스 없음"},
    },
)
def compare_themes(
    theme_ids: list[str] = Query(
        ...,
        description=(
            "비교 대상 theme_id 목록. 반복 (`?theme_ids=1&theme_ids=2`) 또는 "
            "콤마 구분 (`?theme_ids=1,2,3`) 둘 다 지원."
        ),
    ),
    normalize: str = Query("base100", pattern="^base100$"),
    weighting: str = Query("equal", pattern="^(equal|market_cap)$"),
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    base_currency: str = Query("KRW", min_length=3, max_length=8),
    session: Session = Depends(get_db),
) -> ThemeCompareResponse:
    """다중 테마의 aggregate 시리즈를 한 번에 비교.

    각 theme 마다 ``_compute_theme_chart`` 를 호출 후 aggregate 만 응답에 담는다.
    universe_meta 는 마지막 호출 결과의 adjusted_start/end + 전체 affected_assets
    합집합을 채택 (단순화 — Phase 2.1 MVP). Phase 2.2 에서 전체 합집합으로 정밀화
    검토.

    HTTP 매핑:
        - 200: 정상.
        - 404: theme_id 부재 1건이라도.
        - 422: weighting=market_cap / 멤버 0 / 가용 OHLCV 0 (per theme).
    """
    if not theme_ids:
        raise HTTPException(status_code=422, detail="theme_ids 가 비어 있습니다.")

    repo = get_theme_repo(session)

    # 사용자가 콤마 구분 ?theme_ids=1,2,3 으로 보내는 경우 FastAPI 가 list[int]
    # 로 자동 파싱하지 못해 단일 항목 "1,2,3" 으로 들어올 수 있다. 안전망:
    # 각 항목 안에 "," 가 있으면 split.
    expanded: list[int] = []
    for tid in theme_ids:
        if isinstance(tid, int):
            expanded.append(tid)
        else:
            for part in str(tid).split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    expanded.append(int(part))
                except ValueError as exc:
                    raise HTTPException(
                        status_code=422,
                        detail=f"theme_ids 항목 '{part}' 는 정수가 아닙니다.",
                    ) from exc
    if not expanded:
        raise HTTPException(status_code=422, detail="theme_ids 가 비어 있습니다.")

    items: dict[int, ThemeCompareItem] = {}
    last_meta: UniverseMeta | None = None
    affected_union: set[int] = set()

    for tid in expanded:
        _, aggregate_series, meta, _ = _compute_theme_chart(
            session=session,
            repo=repo,
            theme_id=tid,
            start=start,
            end=end,
            weighting=weighting,
        )
        theme = repo.get_theme(tid)
        assert theme is not None  # _compute_theme_chart 가 None 이면 404 했음
        items[tid] = ThemeCompareItem(
            name=theme.name,
            aggregate=_series_to_points(aggregate_series),
        )
        last_meta = meta
        affected_union.update(meta.affected_assets)

    # universe_meta: 마지막 호출의 adjusted 기간 + affected 합집합.
    assert last_meta is not None
    universe_meta = UniverseMeta(
        adjusted_start=last_meta.adjusted_start,
        adjusted_end=last_meta.adjusted_end,
        affected_assets=sorted(affected_union),
        reason=last_meta.reason,
        message=last_meta.message,
    )

    return ThemeCompareResponse(themes=items, universe_meta=universe_meta)


# --- 3. GET /api/themes/{theme_id} -----------------------------------------


@router.get(
    "/{theme_id}",
    response_model=ThemeDetail,
    summary="테마 상세 (활성 멤버 포함)",
    responses=_NOT_FOUND_RESPONSES,
)
def get_theme(
    theme_id: int,
    session: Session = Depends(get_db),
) -> ThemeDetail:
    repo = get_theme_repo(session)
    theme = repo.get_theme(theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail=f"theme_id={theme_id} not found")
    members = repo.list_active_assets(theme_id)
    base = _theme_to_read(theme, member_count=len(members))
    return ThemeDetail(
        theme_id=base.theme_id,
        name=base.name,
        slug=base.slug,
        description=base.description,
        user_id=base.user_id,
        created_at=base.created_at,
        member_count=base.member_count,
        active_members=[_theme_asset_to_read(m) for m in members],
    )


# --- 4. PATCH /api/themes/{theme_id} ---------------------------------------


@router.patch(
    "/{theme_id}",
    response_model=ThemeRead,
    summary="테마 부분 갱신 (name / description)",
    responses=_NOT_FOUND_RESPONSES,
)
def update_theme(
    theme_id: int,
    payload: ThemeUpdate,
    session: Session = Depends(get_db),
) -> ThemeRead:
    repo = get_theme_repo(session)
    try:
        updated = repo.update_theme(
            theme_id,
            name=payload.name,
            description=payload.description,
        )
        session.commit()
    except LookupError as exc:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _theme_to_read(updated)


# --- 5. DELETE /api/themes/{theme_id} --------------------------------------


@router.delete(
    "/{theme_id}",
    status_code=204,
    summary="테마 soft delete (활성 멤버 일괄 종료)",
    responses=_NOT_FOUND_RESPONSES,
)
def delete_theme(
    theme_id: int,
    session: Session = Depends(get_db),
) -> Response:
    """alembic 0005 스키마에 themes.deleted_at 컬럼이 없어 themes row 자체는 보존된다
    (`theme_repository.py` 모듈 docstring 참조). 본 엔드포인트는 활성 멤버 일괄
    종료만 보장.
    """
    repo = get_theme_repo(session)
    try:
        repo.soft_delete_theme(theme_id)
        session.commit()
    except LookupError as exc:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# --- 6. POST /api/themes/{theme_id}/assets ---------------------------------


@router.post(
    "/{theme_id}/assets",
    response_model=ThemeAssetRead,
    status_code=201,
    summary="테마에 자산 추가 (history 자동 append)",
    responses=_NOT_FOUND_OR_CONFLICT_RESPONSES,
)
def add_asset(
    theme_id: int,
    payload: ThemeAssetAdd,
    session: Session = Depends(get_db),
) -> ThemeAssetRead:
    """service.add_asset_to_theme 가 (theme_assets INSERT + history INSERT) 를 단일
    트랜잭션으로 박제. UnitOfWork 가 get_theme_uow 로 주입.

    HTTP 매핑:
        - 201: 추가 성공.
        - 404: theme_id 부재 / asset_id 부재.
        - 409: 이미 active 멤버 (DuplicateActiveMember).
    """
    repo = get_theme_repo(session)
    uow = get_theme_uow(session)

    # 사전 존재 검증 — 404 매핑.
    if repo.get_theme(theme_id) is None:
        raise HTTPException(status_code=404, detail=f"theme_id={theme_id} not found")
    if session.get(AssetModel, payload.asset_id) is None:
        raise HTTPException(
            status_code=404, detail=f"asset_id={payload.asset_id} not found"
        )

    try:
        member = add_asset_to_theme(
            repo,
            uow,
            theme_id=theme_id,
            asset_id=payload.asset_id,
            note=payload.note,
        )
    except DuplicateActiveMember as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    return _theme_asset_to_read(cast(ThemeAssetEntity, member))


# --- 7. DELETE /api/themes/{theme_id}/assets/{asset_id} --------------------


@router.delete(
    "/{theme_id}/assets/{asset_id}",
    status_code=204,
    summary="테마에서 자산 제거 (soft, history 자동 append)",
    responses=_NOT_FOUND_RESPONSES,
)
def remove_asset(
    theme_id: int,
    asset_id: int,
    session: Session = Depends(get_db),
) -> Response:
    """service.remove_asset_from_theme 가 (theme_assets UPDATE removed_at + history
    INSERT) 를 단일 트랜잭션으로 박제.

    HTTP 매핑:
        - 204: 정상 제거.
        - 404: theme_id 부재 / 활성 멤버가 아님 (InactiveMember).
    """
    repo = get_theme_repo(session)
    uow = get_theme_uow(session)

    # 테마 자체 부재 → 404 (service 의 InactiveMember 와 분리해 명확한 메시지).
    if repo.get_theme(theme_id) is None:
        raise HTTPException(status_code=404, detail=f"theme_id={theme_id} not found")

    try:
        remove_asset_from_theme(
            repo,
            uow,
            theme_id=theme_id,
            asset_id=asset_id,
        )
    except InactiveMember as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=204)


# ============================================================================
# TASK-305 — 정규화 차트 API
# ============================================================================
#
# architecture.md V3 § "정규화 차트 사양" (L1038-1045):
#   - rebase=100: 첫 유효 가격을 100 으로 정규화
#   - weighting='equal' (디폴트), 'market_cap' 은 Phase 2.2
#   - universe 시작일 교집합 자동 산출
#
# 데이터 흐름:
#   1) ThemeRepository.list_active_assets(theme_id) → [ThemeAsset]
#   2) AssetModel 일괄 조회 → AssetEntity 로 변환 → Universe 구성
#   3) period_adjustment.adjust_period_for_universe(universe, start, end)
#   4) OHLCV 일괄 조회 (asset_id IN ..., time BETWEEN adjusted_start ~ adjusted_end)
#   5) pandas DataFrame (index=date, columns=asset_id) 구성 + ffill
#   6) normalization.rebase_multi_series → 각 멤버 rebase=100
#   7) compute_theme_aggregate(prices_df, weighting=equal) → 합산 시리즈
#   8) SeriesPoint 응답 변환

# 활성 자산이 0 인 테마 / 가용 OHLCV 가 모두 비어 있는 경우 모두 422 — UI 가
# "테마에 자산을 추가하세요" / "OHLCV 백필이 필요합니다" 를 표시.
_NOT_FOUND_OR_UNPROCESSABLE_RESPONSES: dict[int | str, dict] = {
    **COMMON_ERROR_RESPONSES,
    404: {"model": ErrorResponse, "description": "리소스 없음"},
}

# weighting 디폴트값 (architecture.md L1042 — "equal 디폴트").
# Phase 2.2 에서 'market_cap' 본체가 활성화될 때 본 라우터에서 422 분기를 제거한다.
_WEIGHTING_DEFAULT = "equal"


def _asset_model_to_entity(model: AssetModel) -> AssetEntity:
    """ORM AssetModel → 도메인 AssetEntity 변환 (asset_repository._to_entity 와 동일).

    asset_repository 의 헬퍼를 재사용하지 않고 inline 한 이유: 본 라우터는 단순
    조회 (Universe 구성용) 에만 사용하고 asset_repository 와 동일 import 체인을
    피해 격리성 (theme 트랙) 을 유지하기 위함이다. _to_entity 는 private (앞 _)
    이라 외부 호출 의도가 명확하지 않다.
    """
    return AssetEntity(
        asset_id=model.asset_id,
        symbol=model.symbol,
        market=cast(Market, model.market),
        asset_type=cast(AssetType, model.asset_type),
        currency=model.currency,
        name=model.name,
        meta=model.meta or {},
        active=model.active,
        start_date=model.start_date,
        last_ingested_at=model.last_ingested_at,
    )


def _fetch_ohlcv_prices_df(
    session: Session,
    asset_ids: Iterable[int],
    start: date,
    end: date,
) -> pd.DataFrame:
    """주어진 asset_id 들의 [start, end] OHLCV close 를 pandas DataFrame 으로 적재.

    Returns:
        DataFrame:
            - index: pd.Timestamp (UTC naive date, time=00:00 — base 캘린더 일자)
            - columns: int asset_id
            - value: float close

        자산별 OHLCV row 가 0 건이면 해당 컬럼이 DataFrame 에 없다.
        index 는 모든 자산의 거래일 합집합. forward-fill / rebase 는 호출자
        책임 (정규화 도메인 함수가 NaN 을 보존하므로).
    """
    asset_id_list = list(asset_ids)
    if not asset_id_list:
        return pd.DataFrame()

    # 단일 IN 쿼리 — N+1 회피.
    stmt = (
        select(OhlcvModel.asset_id, OhlcvModel.time, OhlcvModel.close)
        .where(
            OhlcvModel.asset_id.in_(asset_id_list),
            OhlcvModel.time >= datetime.combine(start, time.min, tzinfo=timezone.utc),
            OhlcvModel.time <= datetime.combine(end, time.max, tzinfo=timezone.utc),
        )
        .order_by(OhlcvModel.asset_id, OhlcvModel.time)
    )
    rows = session.execute(stmt).all()
    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(
        [
            {
                "asset_id": r.asset_id,
                # tz-aware → tz-naive UTC 일자로 정규화. base 캘린더 정렬은
                # pivot 후 호출자가 reindex 로 한다.
                "date": pd.Timestamp(r.time).tz_convert("UTC").normalize().tz_localize(None),
                "close": float(r.close),
            }
            for r in rows
        ]
    )
    # 같은 (asset_id, date) 가 hypertable 에서 1행 이지만, 방어적으로 last 채택.
    pivot = df.pivot_table(
        index="date", columns="asset_id", values="close", aggfunc="last"
    )
    pivot = pivot.sort_index()
    return pivot


def _series_to_points(series: pd.Series) -> list[SeriesPoint]:
    """pandas Series (DatetimeIndex, float) → list[SeriesPoint].

    NaN 항목은 응답에서 제외 (frontend recharts 가 누락 일자를 자연스럽게
    line gap 으로 처리하지 않으므로). 정렬은 index 시간순.
    """
    points: list[SeriesPoint] = []
    for ts, val in series.items():
        if pd.isna(val):
            continue
        # Decimal 직렬화: rebase=100 이라 ~소수점 6자리 정밀도면 충분.
        # repr(float) 대신 f"{val:.6f}" 로 string 화 → Decimal → JSON.
        points.append(
            SeriesPoint(
                time=pd.Timestamp(ts).to_pydatetime(),
                value=Decimal(f"{float(val):.6f}"),
            )
        )
    return points


def _build_universe_meta_from_period(
    adjustment, ohlcv_df: pd.DataFrame, requested_asset_ids: list[int]
) -> UniverseMeta:
    """PeriodAdjustment + OHLCV 가용성 → UniverseMeta 응답.

    affected_assets 는 asset_id (int) 목록 — period_adjustment 의 symbol 튜플
    매핑 외에 OHLCV 가 비어 있어 차트에서 빠진 자산 (전체 NaN) 까지 합쳐 통지.
    """
    # OHLCV 0행인 자산 = 차트에서 빠진다.
    missing_ohlcv = [aid for aid in requested_asset_ids if aid not in ohlcv_df.columns]
    affected = sorted(set(missing_ohlcv))
    message = adjustment.message
    if missing_ohlcv:
        message = (
            f"{message} (가용 OHLCV 가 없는 자산 {len(missing_ohlcv)}건은 차트에서 제외됨)"
        )
    return UniverseMeta(
        adjusted_start=adjustment.adjusted_start,
        adjusted_end=adjustment.adjusted_end,
        affected_assets=affected,
        reason=adjustment.reason,
        message=message,
    )


def _compute_theme_chart(
    session: Session,
    repo,
    theme_id: int,
    start: date | None,
    end: date | None,
    weighting: str,
) -> tuple[pd.DataFrame, pd.Series, UniverseMeta, list[int]]:
    """단일 테마 chart 계산 공통 로직.

    Endpoint A/B 가 공유. members 차트가 필요한 A 와 aggregate 만 필요한 B 가
    동일한 정규화 산식을 거치도록 함.

    Returns:
        (rebased_df, aggregate_series, universe_meta, member_asset_ids)
            - rebased_df: rebase=100 적용된 멤버 시리즈 DataFrame
            - aggregate_series: weighting 적용 합산 시리즈
            - universe_meta: 응답용 UniverseMeta
            - member_asset_ids: 활성 멤버 asset_id 목록

    Raises:
        HTTPException 404: theme_id 부재
        HTTPException 422: 활성 멤버 0 / 가용 OHLCV 0 / weighting=market_cap
    """
    # 0) weighting 사전 검증
    if weighting == "market_cap":
        raise HTTPException(
            status_code=422,
            detail="weighting='market_cap' 은 Phase 2.2 에서 지원 예정입니다.",
        )
    if weighting != "equal":
        raise HTTPException(
            status_code=422,
            detail=f"weighting='{weighting}' 은 지원하지 않습니다 (equal 만 지원).",
        )

    # 1) 테마 존재 + 활성 멤버 조회
    theme = repo.get_theme(theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail=f"theme_id={theme_id} not found")

    members = repo.list_active_assets(theme_id)
    if not members:
        raise HTTPException(
            status_code=422,
            detail=f"theme_id={theme_id} 에 활성 자산이 없습니다.",
        )
    member_asset_ids = [m.asset_id for m in members]

    # 2) AssetModel 일괄 조회 → AssetEntity → Universe
    asset_models = (
        session.execute(
            select(AssetModel).where(AssetModel.asset_id.in_(member_asset_ids))
        )
        .scalars()
        .all()
    )
    asset_entities = tuple(_asset_model_to_entity(m) for m in asset_models)
    universe = Universe(assets=asset_entities)

    # 3) 기간 결정: start/end 미지정이면 universe 의 common_period 우선,
    #    그래도 부족하면 안전한 폴백 (1970-01-01 ~ 오늘).
    common = universe.common_period()
    if common is not None:
        default_start, default_end = common
    else:
        default_start, default_end = date(1970, 1, 1), date.today()

    requested_start = start if start is not None else default_start
    requested_end = end if end is not None else default_end

    adjustment = adjust_period_for_universe(
        universe, requested_start=requested_start, requested_end=requested_end
    )

    # 4) OHLCV 일괄 적재
    prices_df = _fetch_ohlcv_prices_df(
        session,
        asset_ids=member_asset_ids,
        start=adjustment.adjusted_start,
        end=adjustment.adjusted_end,
    )

    # 5) base 캘린더 정렬은 V3 § "멀티 마켓 캘린더" 정책상 base_currency 의
    #    거래일 grid 가 기준이지만, 정규화 차트는 표시용이라 prices_df 의
    #    자연 합집합 index 를 그대로 사용하고 forward-fill 만 적용한다. (캘린더
    #    정확도가 필요한 백테스트 회계는 engine.py 가 별도 처리.)
    if not prices_df.empty:
        prices_df = prices_df.ffill()

    if prices_df.empty:
        # 가용 OHLCV 0 — 차트 의미 없음. 422.
        raise HTTPException(
            status_code=422,
            detail=(
                f"theme_id={theme_id} 의 활성 자산 {len(member_asset_ids)}개에 대해 "
                f"기간 [{adjustment.adjusted_start} ~ {adjustment.adjusted_end}] 의 "
                "가용 OHLCV 가 없습니다. 자산 백필 후 다시 시도하세요."
            ),
        )

    # 6) rebase + aggregate
    rebased_df = rebase_multi_series(prices_df, base_value=Decimal("100"))
    aggregate_series = compute_theme_aggregate(rebased_df, weighting="equal")

    # 7) universe_meta 구성 (OHLCV 누락 자산 합산 통지 포함)
    universe_meta = _build_universe_meta_from_period(
        adjustment, prices_df, member_asset_ids
    )
    return rebased_df, aggregate_series, universe_meta, member_asset_ids


# --- 8. GET /api/themes/{theme_id}/chart -----------------------------------


@router.get(
    "/{theme_id}/chart",
    response_model=ThemeChartResponse,
    summary="정규화 차트 (rebase=100, members + aggregate)",
    responses=_NOT_FOUND_OR_UNPROCESSABLE_RESPONSES,
)
def get_theme_chart(
    theme_id: int,
    normalize: str = Query("base100", pattern="^base100$"),
    weighting: str = Query(
        _WEIGHTING_DEFAULT,
        pattern="^(equal|market_cap)$",
        description="market_cap 은 Phase 2.2 — 현재 422 반환",
    ),
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    base_currency: str = Query("KRW", min_length=3, max_length=8),
    session: Session = Depends(get_db),
) -> ThemeChartResponse:
    """단일 테마의 정규화 차트.

    architecture.md V3 § "정규화 차트 사양":
        - rebase=100 (현재 유일 지원)
        - weighting=equal (현재 유일 지원)
        - universe 시작일 교집합 자동 산출 + 한국어 통지

    HTTP 매핑:
        - 200: 정상 — members(asset_id→series) + aggregate + universe_meta.
        - 404: theme_id 부재.
        - 422: 활성 멤버 0 / 가용 OHLCV 0 / weighting=market_cap.
    """
    repo = get_theme_repo(session)
    rebased_df, aggregate_series, universe_meta, _member_ids = _compute_theme_chart(
        session=session,
        repo=repo,
        theme_id=theme_id,
        start=start,
        end=end,
        weighting=weighting,
    )

    # members: asset_id → SeriesPoint[]. OHLCV 가 0 인 자산은 rebased_df 컬럼에
    # 없으므로 자연 제외 (universe_meta.affected_assets 에는 등재됨).
    members: dict[int, list[SeriesPoint]] = {}
    for asset_id in rebased_df.columns:
        members[int(asset_id)] = _series_to_points(rebased_df[asset_id])

    return ThemeChartResponse(
        members=members,
        aggregate=_series_to_points(aggregate_series),
        universe_meta=universe_meta,
    )
