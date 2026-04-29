"""전역 예외 핸들러 — 모든 4xx/5xx 응답을 ErrorResponse 계약으로 통일.

architecture.md V2 § "에러 응답 계약" (L450~) 준수:
- 응답 본문: {"error": {"stage", "type", "message", "request_ctx", "trace_id"}}
- 서버 로그: `trace_id=<uuid> stage=<stage> ctx=<ctx>` 접두사로 stacktrace 출력

핸들러는 `core/` 디렉토리 충돌(TASK-002 와 병렬 실행)을 회피하기 위해 의도적으로
`backend/app/api/_error.py` 에 배치한다.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import ErrorDetail, ErrorResponse

_logger = logging.getLogger("app.api.error")


def _build_request_ctx(request: Request) -> dict[str, Any]:
    """요청 식별 정보(path/method/query)를 dict 로 추출."""

    return {
        "path": request.url.path,
        "method": request.method,
        "query": dict(request.query_params),
    }


def _emit(
    *,
    trace_id: str,
    stage: str,
    type_name: str,
    message: str,
    request_ctx: dict[str, Any],
    status_code: int,
    exc: BaseException,
) -> JSONResponse:
    """ErrorResponse 본문을 만들고, 서버 로그에 trace_id/stage/ctx 접두사로 기록."""

    # 서버 로그는 클라이언트가 trace_id 만 보고 stacktrace 까지 grep 할 수 있게 prefix 한다.
    _logger.error(
        "trace_id=%s stage=%s ctx=%s status=%s exc=%s",
        trace_id,
        stage,
        request_ctx,
        status_code,
        type_name,
        exc_info=exc,
    )
    payload = ErrorResponse(
        error=ErrorDetail(
            stage=stage,
            type=type_name,
            message=message,
            request_ctx=request_ctx,
            trace_id=trace_id,
        )
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


async def _http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """FastAPI/Starlette HTTPException → ErrorResponse."""

    trace_id = uuid.uuid4().hex
    # HTTPException 의 detail 이 dict 면 그대로, 아니면 문자열로 노출한다.
    detail = exc.detail
    message = detail if isinstance(detail, str) else str(detail)
    return _emit(
        trace_id=trace_id,
        stage=request.url.path or "http",
        type_name=exc.__class__.__name__,
        message=message,
        request_ctx=_build_request_ctx(request),
        status_code=exc.status_code,
        exc=exc,
    )


async def _validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Pydantic 요청 검증 실패 → ErrorResponse (stage='validation')."""

    trace_id = uuid.uuid4().hex
    ctx = _build_request_ctx(request)
    # 어느 필드가 실패했는지 ctx 에 함께 노출 — 클라이언트가 폼에 즉시 표시 가능.
    ctx["errors"] = exc.errors()
    return _emit(
        trace_id=trace_id,
        stage="validation",
        type_name=exc.__class__.__name__,
        message="요청 본문/쿼리가 스키마를 만족하지 않습니다.",
        request_ctx=ctx,
        status_code=422,
        exc=exc,
    )


async def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """예측하지 못한 예외 → ErrorResponse (stage='internal', 500)."""

    trace_id = uuid.uuid4().hex
    return _emit(
        trace_id=trace_id,
        stage="internal",
        type_name=exc.__class__.__name__,
        message="서버 내부 오류가 발생했습니다. trace_id 로 지원에 문의하세요.",
        request_ctx=_build_request_ctx(request),
        status_code=500,
        exc=exc,
    )


def add_exception_handlers(app: FastAPI) -> None:
    """FastAPI 앱에 4xx/5xx 통합 핸들러 3종을 등록."""

    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(RequestValidationError, _validation_exception_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)
