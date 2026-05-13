"""Quant Lab API FastAPI 앱 엔트리.

이 파일은 앱 조립만 담당한다. 비즈니스 로직은 `app/domain/`, 라우팅은 `app/api/` 에 둔다.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic.json_schema import models_json_schema

from app import __version__
from app.api import (
    add_exception_handlers,
    assets_router,
    backtests_router,
    health_router,
    strategies_router,
    themes_router,
)
from app.schemas.common import (
    ErrorDetail,
    ErrorResponse,
    HealthResponse,
    PaginatedResponse,
    TimestampedModel,
)
from app.scheduler import build_scheduler

# 핸들러가 stacktrace 를 노출할 수 있도록 root logger 를 한 번 설정한다.
# (uvicorn 도 자체 logger 를 갖지만, app.api.error 모듈은 별도 logger 라 영향 없음.)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


def _build_custom_openapi(app: FastAPI):
    """라우트가 직접 사용하지 않더라도 cross-endpoint base 스키마를
    `components.schemas` 에 강제 노출하는 OpenAPI 커스터마이저.

    FastAPI 의 자동 OpenAPI 는 라우트가 실제 reference 한 모델만 components 에
    포함하므로, 후속 태스크(TASK-061/062)에서 활용할 base 스키마들을 미리 노출한다.
    """

    def _custom_openapi() -> dict[str, Any]:
        if app.openapi_schema is not None:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # PaginatedResponse 는 generic 이라 직접 노출 시 `T` 없는 base shape 가 필요하다.
        # PaginatedResponse[HealthResponse] 의 schema 를 참조하되, $defs 를 컴포넌트로 승격한다.
        extra_models = [
            (ErrorResponse, "validation"),
            (ErrorDetail, "validation"),
            (PaginatedResponse[HealthResponse], "validation"),
            (TimestampedModel, "validation"),
        ]
        # generic instantiation 의 ref name 을 base 명("PaginatedResponse")로 노출.
        _, defs_top = models_json_schema(extra_models, ref_template="#/components/schemas/{model}")  # type: ignore[arg-type]
        components = schema.setdefault("components", {}).setdefault("schemas", {})
        for name, sub in defs_top.get("$defs", {}).items():
            # 제네릭 instantiation (예: PaginatedResponse_HealthResponse_) 은
            # 베이스 이름(PaginatedResponse) 으로 정규화한다.
            normalized = "PaginatedResponse" if name.startswith("PaginatedResponse") else name
            components.setdefault(normalized, sub)

        app.openapi_schema = schema
        return schema

    return _custom_openapi


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """FastAPI lifespan — APScheduler 기반 cron 잡 부트스트랩.

    KR 18:00 / US 07:00 / Crypto 09:00 KST 에 backfill_active_assets 자동 실행.
    """
    scheduler = build_scheduler()
    scheduler.start()
    app.state.scheduler = scheduler
    logger = logging.getLogger(__name__)
    logger.info("APScheduler started: %s", [(j.id, j.name) for j in scheduler.get_jobs()])
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler shutdown")


def create_app() -> FastAPI:
    """FastAPI 인스턴스 생성. 테스트에서도 호출 가능하도록 팩토리화."""

    app = FastAPI(
        title="Quant Lab API",
        version=__version__,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=_lifespan,
    )

    # 비개발자 사용자가 Next.js 프런트(`NEXT_PUBLIC_API_BASE_URL`)에서 호출하는 것을 허용.
    # 프로덕션에서는 운영 도메인을 추가해야 한다.
    # stock-backtest frontend 는 systemd 영속화로 3001 포트 사용. dev 디폴트 3000 도 함께 허용.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(assets_router)
    app.include_router(strategies_router)
    app.include_router(backtests_router)
    app.include_router(themes_router)

    app.openapi = _build_custom_openapi(app)  # type: ignore[method-assign]

    return app


app = create_app()
