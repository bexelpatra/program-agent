"""Shared FastAPI dependencies (settings, ES client, project paths).

The settings YAML path is captured at ``create_app`` time and injected into
request-scoped dependencies via ``app.state``. This avoids re-loading the
config on every request while still letting tests pass custom paths.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import Request

from src import es_client


# ---------------------------------------------------------------------------
# Project-root resolution
# ---------------------------------------------------------------------------

#: Repository-relative path to the abc-english project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_project_path(rel: str) -> Path:
    """Resolve a path relative to the project root (``projects/abc-english``)."""
    return PROJECT_ROOT / rel


# ---------------------------------------------------------------------------
# Request-scoped dependencies
# ---------------------------------------------------------------------------


def get_settings(request: Request) -> Dict[str, Any]:
    """Return the settings dict stashed on ``app.state`` by :func:`create_app`."""
    settings = getattr(request.app.state, "settings", None)
    if settings is None:
        settings_path = getattr(request.app.state, "settings_path", None)
        settings = es_client.load_settings(Path(settings_path) if settings_path else None)
        request.app.state.settings = settings
    return settings


def get_es(request: Request):
    """Return a (lazily initialised) Elasticsearch client."""
    settings = get_settings(request)
    return es_client.get_client(settings=settings)


def get_index(request: Request, index_key: str) -> str:
    """Resolve a logical index key (``episodes`` / ``sentences`` / ...)."""
    settings = get_settings(request)
    return es_client.get_index_name(index_key, settings=settings)
