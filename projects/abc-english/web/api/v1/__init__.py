"""/api/v1/ namespace — versioned API for the abc-english-app client.

All routers under this package share the Bearer auth dependency defined in
``deps.py`` and should be included on the top-level app via
:func:`build_v1_router`.
"""

from __future__ import annotations

from fastapi import APIRouter

from . import audio as audio_v1
from . import episodes as episodes_v1
from . import lookup as lookup_v1
from . import manifest as manifest_v1
from . import notebook as notebook_v1
from .deps import require_bearer


def build_v1_router() -> APIRouter:
    """Return the composed /api/v1 router with Bearer auth applied."""
    router = APIRouter(prefix="/api/v1", dependencies=[require_bearer()])
    router.include_router(episodes_v1.router)
    router.include_router(audio_v1.router)
    router.include_router(manifest_v1.router)
    router.include_router(lookup_v1.router)
    router.include_router(notebook_v1.router)
    return router


__all__ = ["build_v1_router", "require_bearer"]
