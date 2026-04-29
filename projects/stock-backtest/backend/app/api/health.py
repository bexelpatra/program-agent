"""GET /api/health — liveness 엔드포인트."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app import __version__
from app.schemas.common import ErrorResponse, HealthResponse

router = APIRouter(prefix="/api", tags=["health"])

# 모든 엔드포인트에 일관된 에러 응답 형식을 노출하기 위한 공통 responses.
# 새 라우터를 추가할 때 그대로 import 해 사용한다.
COMMON_ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorResponse, "description": "잘못된 요청"},
    422: {"model": ErrorResponse, "description": "요청 검증 실패"},
    500: {"model": ErrorResponse, "description": "서버 내부 오류"},
}


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Liveness check",
    responses=COMMON_ERROR_RESPONSES,
)
def get_health() -> HealthResponse:
    """배포된 백엔드 버전과 함께 'ok' 를 반환한다."""

    return HealthResponse(status="ok", version=__version__)
