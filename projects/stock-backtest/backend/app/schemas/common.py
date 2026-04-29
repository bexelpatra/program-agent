"""Cross-endpoint Pydantic base schemas.

이 모듈은 도메인에 특화되지 않은 공통 응답·요청 스키마만 정의한다.
- ErrorResponse / ErrorDetail: V3 architecture.md V2 § "에러 응답 계약" (L450~) 준수.
- PaginatedResponse[T]: 리스트 엔드포인트 공통 페이지네이션 wrapper.
- TimestampedModel: created_at/updated_at 가 노출될 때 사용하는 mixin.
- HealthResponse: GET /api/health 전용.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """단일 에러의 stage/type/message/ctx/trace_id 페이로드."""

    model_config = ConfigDict(frozen=True)

    stage: str = Field(
        ...,
        description="에러가 발생한 처리 단계 (예: 'validation', 'resolve_universe', 'internal').",
    )
    type: str = Field(
        ...,
        description="원본 예외 클래스명 (예: 'RequestValidationError', 'ValueError').",
    )
    message: str = Field(..., description="사용자에게 노출 가능한 한국어 메시지.")
    request_ctx: dict[str, Any] = Field(
        default_factory=dict,
        description="요청 식별을 돕는 컨텍스트 (path/method/query 등).",
    )
    trace_id: str = Field(
        ...,
        description="요청별 trace UUID. 서버 로그와 클라이언트 응답 교차 조회용.",
    )


class ErrorResponse(BaseModel):
    """모든 4xx/5xx 응답의 최상위 wrapper."""

    model_config = ConfigDict(frozen=True)

    error: ErrorDetail


class PaginatedResponse(BaseModel, Generic[T]):
    """리스트 엔드포인트 공통 응답 (items/total/page/page_size)."""

    items: list[T]
    total: int = Field(..., ge=0)
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1)


class TimestampedModel(BaseModel):
    """created_at/updated_at 를 노출하는 도메인 모델용 mixin."""

    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """GET /api/health 응답."""

    status: Literal["ok"]
    version: str
