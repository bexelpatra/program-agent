"""자산 API 라우터.

엔드포인트:
- GET    /api/assets              — 카탈로그 검색 (q/market/asset_type/limit/offset)
- POST   /api/assets               — 사용자 자유 추가 (TASK-031 register_asset 호출)
- GET    /api/assets/{asset_id}    — 단일 자산 상세
- GET    /api/assets/{asset_id}/ohlcv — 기간 OHLCV (start/end)

architecture.md V3 § "자산 카탈로그 + 사용자 자유 추가" L532-538 + § "V2 API" L425-429 근거.
도메인 레이어(`app.domain.asset.registration`) 는 HTTP 무관 — 본 라우터가 HTTP 경계에서만
HTTPException 으로 변환한다 (코더 가이드 § 8 "오류 처리 — 경계에서만").
"""
from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.health import COMMON_ERROR_RESPONSES
from app.data.sources.pykrx_source import PykrxSource
from app.data.sources.yfinance_source import YfinanceSource
from app.dependencies import get_asset_repo, get_db
from app.domain.asset.entity import Asset, AssetType, Market
from app.domain.asset.registration import (
    AlreadyRegistered,
    BackfillEnqueuer,
    RegistrationRequest,
    TickerValidationFailed,
    TickerValidator,
    ValidationOutcome,
    register_asset,
)
from app.models.ohlcv import Ohlcv
from app.schemas.asset import (
    AssetCreate,
    AssetCreateResponse,
    AssetRead,
    OhlcvPoint,
)
from app.schemas.common import PaginatedResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assets", tags=["assets"])


# --- 변환 헬퍼 ------------------------------------------------------------

def _to_read(asset: Asset) -> AssetRead:
    """도메인 Asset → AssetRead 응답 DTO 변환."""

    return AssetRead(
        asset_id=asset.asset_id,
        symbol=asset.symbol,
        market=asset.market,
        asset_type=asset.asset_type,
        currency=asset.currency,
        name=asset.name,
        meta=asset.meta or {},
        active=asset.active,
        start_date=asset.start_date,
        last_ingested_at=asset.last_ingested_at,
    )


def _decimal_or_none(value: Any) -> float | None:
    """ORM Numeric → float | None. None 보존."""

    return float(value) if value is not None else None


# --- TASK-031 Protocol 어댑터 (MVP) --------------------------------------

class _RoutingValidator:
    """TickerValidator Protocol 의 라우팅 구현.

    market 별로 yfinance / pykrx 를 선택하고, source 의 TickerValidation 을
    domain 의 ValidationOutcome 으로 변환한다 (어댑터는 source 타입을 누설하지 않음).
    """

    def __init__(self, market: str):
        self._source = PykrxSource() if market == "KR" else YfinanceSource()

    def validate_ticker(self, symbol: str) -> ValidationOutcome:
        result = self._source.validate_ticker(symbol)
        return ValidationOutcome(
            ticker=result.ticker,
            exists=result.exists,
            has_min_history=result.has_min_history,
            earliest_date=result.earliest,
            note=result.note,
        )


class _LoggingEnqueuer:
    """BackfillEnqueuer Protocol 의 MVP 구현 — 로깅만 한다.

    TODO(TASK-070+): 실제 BackfillQueue 인스턴스를 `app.state.backfill_queue` 로
    lifespan 에서 주입하고 그 큐에 push 한다. 지금은 placeholder.
    """

    def enqueue(self, asset_id: int) -> None:
        logger.info(
            "backfill enqueue requested asset_id=%d (placeholder — actual queue wired later)",
            asset_id,
        )


# --- 엔드포인트 -----------------------------------------------------------

@router.get(
    "",
    response_model=PaginatedResponse[AssetRead],
    summary="자산 카탈로그 검색",
    responses=COMMON_ERROR_RESPONSES,
)
def list_assets(
    q: str | None = Query(None, description="symbol/name prefix (대소문자 무시)"),
    market: Market | None = Query(None, description="시장 필터 (KR/US/CRYPTO)"),
    asset_type: AssetType | None = Query(
        None, description="자산 타입 필터 (EQUITY_INDEX/ETF/BOND/COMMODITY/CRYPTO)"
    ),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_db),
) -> PaginatedResponse[AssetRead]:
    """active=true 인 자산만 반환. 정확한 total 카운트는 향후 별도 쿼리로 보강."""

    repo = get_asset_repo(session)
    items = repo.search(
        q=q,
        market=market,
        asset_type=asset_type,
        limit=limit,
        offset=offset,
    )
    page = (offset // limit) + 1 if limit > 0 else 1
    return PaginatedResponse(
        items=[_to_read(a) for a in items],
        total=len(items),
        page=page,
        page_size=limit,
    )


@router.get(
    "/{asset_id}",
    response_model=AssetRead,
    summary="자산 상세",
    responses=COMMON_ERROR_RESPONSES,
)
def get_asset(
    asset_id: int,
    session: Session = Depends(get_db),
) -> AssetRead:
    repo = get_asset_repo(session)
    asset = repo.find_by_id(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"asset_id={asset_id} not found")
    return _to_read(asset)


@router.post(
    "",
    response_model=AssetCreateResponse,
    status_code=201,
    summary="자산 자유 추가",
    responses=COMMON_ERROR_RESPONSES,
)
def create_asset(
    payload: AssetCreate,
    session: Session = Depends(get_db),
) -> AssetCreateResponse:
    """사용자 자유 추가 워크플로우 (TASK-031 register_asset).

    HTTP 매핑:
        - 201: 등록 성공 (백필은 비동기, note 로 진행 상황 안내)
        - 409: AlreadyRegistered (동일 symbol+market active 자산)
        - 422: TickerValidationFailed (시장 데이터 소스 검증 실패)
    """

    repo = get_asset_repo(session)
    request = RegistrationRequest(
        symbol=payload.symbol,
        market=payload.market,
        asset_type=payload.asset_type,
        currency=payload.currency,
        name=payload.name,
        meta=payload.meta,
    )
    validator: TickerValidator = _RoutingValidator(payload.market)
    enqueuer: BackfillEnqueuer = _LoggingEnqueuer()

    try:
        result = register_asset(request, repo, validator, enqueuer)
    except AlreadyRegistered as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except TickerValidationFailed as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    session.commit()
    return AssetCreateResponse(
        asset=_to_read(result.asset),
        backfill_enqueued=result.backfill_enqueued,
        note=result.note,
    )


@router.get(
    "/{asset_id}/ohlcv",
    response_model=list[OhlcvPoint],
    summary="자산 일봉 OHLCV 조회",
    responses=COMMON_ERROR_RESPONSES,
)
def get_ohlcv(
    asset_id: int,
    start: date = Query(..., description="시작일 (포함)"),
    end: date = Query(..., description="종료일 (포함)"),
    session: Session = Depends(get_db),
) -> list[OhlcvPoint]:
    """[start, end] 구간 일봉. 미존재 자산은 404, 빈 구간은 빈 리스트."""

    repo = get_asset_repo(session)
    if repo.find_by_id(asset_id) is None:
        raise HTTPException(status_code=404, detail=f"asset_id={asset_id} not found")
    if start > end:
        raise HTTPException(
            status_code=422, detail=f"start ({start}) must be <= end ({end})"
        )

    rows = (
        session.execute(
            select(Ohlcv)
            .where(
                Ohlcv.asset_id == asset_id,
                Ohlcv.time >= datetime.combine(start, datetime.min.time()),
                Ohlcv.time <= datetime.combine(end, datetime.max.time()),
            )
            .order_by(Ohlcv.time)
        )
        .scalars()
        .all()
    )

    return [
        OhlcvPoint(
            time=row.time,
            open=_decimal_or_none(row.open),
            high=_decimal_or_none(row.high),
            low=_decimal_or_none(row.low),
            close=float(row.close),
            adj_close=_decimal_or_none(row.adj_close),
            volume=_decimal_or_none(row.volume),
        )
        for row in rows
    ]
