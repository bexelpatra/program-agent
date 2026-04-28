"""Shared dependencies for the /api/v1 namespace.

The only v1-specific dependency is :func:`require_bearer`, which enforces an
``Authorization: Bearer <token>`` header. The expected token is sourced from
``settings.api_token`` (YAML) or the ``ABC_API_TOKEN`` environment variable
(env wins over YAML when both are present). An empty token at startup is a
configuration error and raises :class:`RuntimeError` when resolved.

Design note: authentication lives here instead of the shared ``web/deps.py``
because the v0 API is intentionally unauthenticated (local-only). Only the v1
surface (consumed by the mobile app) requires a token.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import Depends, Header, HTTPException, Request, status


_MISSING_TOKEN_MSG = (
    "api_token is not configured. Set 'api_token' in settings.yaml or the "
    "ABC_API_TOKEN environment variable."
)


def resolve_api_token(settings: Optional[Dict[str, Any]] = None) -> str:
    """Resolve the expected Bearer token.

    Precedence: ``ABC_API_TOKEN`` env var > ``settings['api_token']``.

    Raises:
        RuntimeError: When neither source yields a non-empty string.
    """
    env_token = os.environ.get("ABC_API_TOKEN")
    if env_token and env_token.strip():
        return env_token.strip()

    if settings is not None:
        yaml_token = settings.get("api_token")
        if isinstance(yaml_token, str) and yaml_token.strip():
            return yaml_token.strip()

    raise RuntimeError(_MISSING_TOKEN_MSG)


def _get_expected_token(request: Request) -> str:
    settings = getattr(request.app.state, "settings", None) or {}
    return resolve_api_token(settings)


async def verify_bearer(
    request: Request,
    authorization: Optional[str] = Header(default=None),
) -> None:
    """Validate the ``Authorization: Bearer <token>`` header.

    Raises:
        HTTPException(401): Header missing, malformed, or token mismatch.
        HTTPException(500): Server token is not configured.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, value = authorization.partition(" ")
    if scheme.lower() != "bearer" or not value.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid Authorization scheme",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        expected = _get_expected_token(request)
    except RuntimeError as exc:
        # Mis-configuration: no server-side token. Fail closed with 500 so the
        # operator notices. (Startup also raises — see app.py.)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    if value.strip() != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_bearer() -> Any:
    """Return a FastAPI dependency enforcing Bearer auth."""
    return Depends(verify_bearer)
