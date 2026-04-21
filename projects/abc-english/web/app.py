"""FastAPI application factory for the abc-english web UI.

Usage (uvicorn)::

    uvicorn --factory web.app:create_app --host 0.0.0.0 --port 8000

The factory accepts a ``settings_path`` so tests can swap YAMLs at will.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional, Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src import es_client
from src.ollama_client import verify_ollama_model

from .api import audio as audio_api
from .api import episodes as episodes_api
from .api import lookup as lookup_api
from .api import notebook as notebook_api
from .api import study_helper as study_helper_api
from .routes import pages as pages_routes

_WEB_DIR = Path(__file__).resolve().parent
_STATIC_DIR = _WEB_DIR / "static"

logger = logging.getLogger(__name__)


def create_app(settings_path: Optional[Union[str, Path]] = None) -> FastAPI:
    """Build the FastAPI app.

    Args:
        settings_path: Optional YAML settings path. Falls back to the
            bundled ``config/settings.yaml`` when omitted.

    Returns:
        A fully-wired :class:`FastAPI` instance (not yet served).
    """
    if settings_path is None:
        env_path = os.environ.get("ABC_CONFIG")
        if env_path:
            settings_path = env_path
    resolved = Path(settings_path) if settings_path else None
    settings = es_client.load_settings(resolved)

    app = FastAPI(title="abc-english study API", version="1.0.0")
    app.state.settings = settings
    app.state.settings_path = str(resolved) if resolved else None

    # CORS (local dev only — trust everything).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Range", "Content-Length", "Accept-Ranges"],
    )

    # Mount API routers.
    app.include_router(episodes_api.router)
    app.include_router(audio_api.router)
    app.include_router(lookup_api.router)
    app.include_router(notebook_api.router)
    app.include_router(study_helper_api.router)

    # HTML pages (templates + static assets).
    app.include_router(pages_routes.router)
    if _STATIC_DIR.exists():
        app.mount(
            "/static",
            StaticFiles(directory=str(_STATIC_DIR)),
            name="static",
        )

    @app.on_event("startup")
    async def _verify_ollama_on_startup() -> None:  # pragma: no cover - best-effort
        try:
            result = await verify_ollama_model(settings)
            if not result.get("ok"):
                logger.warning(
                    "Ollama model verification failed: %s",
                    result.get("warning", "unknown"),
                )
            else:
                logger.info("Ollama model verification OK")
        except Exception as exc:
            logger.warning("Ollama verification raised: %s", exc)

    @app.get("/api/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app
