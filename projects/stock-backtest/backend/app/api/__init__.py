"""FastAPI 라우터 + 전역 예외 핸들러 re-export."""

from app.api._error import add_exception_handlers
from app.api.assets import router as assets_router
from app.api.backtests import router as backtests_router
from app.api.health import router as health_router
from app.api.strategies import router as strategies_router

__all__ = [
    "add_exception_handlers",
    "assets_router",
    "backtests_router",
    "health_router",
    "strategies_router",
]
