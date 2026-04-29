"""전략 API 라우터.

GET /api/strategies — allocator/filter 목록 + 각 전략의 pydantic params JSON Schema.
프런트가 이 응답을 받아 전략 빌더 UI 의 폼을 자동 생성한다 (UI/UX 원칙 1).

architecture.md V3 § "V2 API" L426 + Quant Lab CLAUDE.md L26 (MVP 프리셋: allocator 3,
filter 2) 근거.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.api.health import COMMON_ERROR_RESPONSES
from app.domain.allocators import (
    AllWeather,
    AllWeatherParams,
    EqualWeight,
    EqualWeightParams,
    FixedWeight,
    FixedWeightParams,
)
from app.domain.filters import (
    Momentum,
    MomentumParams,
    MovingAverage,
    MovingAverageParams,
)
from app.schemas.strategy import StrategyDescriptor, StrategyListResponse

router = APIRouter(prefix="/api/strategies", tags=["strategies"])


@router.get(
    "",
    response_model=StrategyListResponse,
    summary="전략 목록 + JSON Schema",
    responses=COMMON_ERROR_RESPONSES,
)
def list_strategies() -> StrategyListResponse:
    """allocator 3종 + filter 2종 + 각 전략 파라미터 JSON Schema 반환.

    description 은 한국어 (UI/UX 원칙 2: 비개발자 한국어 우선).
    """

    allocators = [
        StrategyDescriptor(
            name=FixedWeight.name,
            type="allocator",
            params_schema=FixedWeightParams.model_json_schema(),
            description="고정 비중 자산 배분",
        ),
        StrategyDescriptor(
            name=AllWeather.name,
            type="allocator",
            params_schema=AllWeatherParams.model_json_schema(),
            description=(
                "올웨더 (주식 30 / 장기채 40 / 중기채 15 / 금 7.5 / 원자재 7.5)"
            ),
        ),
        StrategyDescriptor(
            name=EqualWeight.name,
            type="allocator",
            params_schema=EqualWeightParams.model_json_schema(),
            description="균등 비중 (1/N)",
        ),
    ]
    filters = [
        StrategyDescriptor(
            name=MovingAverage.name,
            type="filter",
            params_schema=MovingAverageParams.model_json_schema(),
            description="이동평균 위/아래 필터",
        ),
        StrategyDescriptor(
            name=Momentum.name,
            type="filter",
            params_schema=MomentumParams.model_json_schema(),
            description="모멘텀 (lookback 수익률) 필터",
        ),
    ]
    return StrategyListResponse(allocators=allocators, filters=filters)
