"""Web UI package for abc-english (FastAPI backend).

Expose :func:`create_app` from :mod:`web.app` for use by ``uvicorn`` and tests.
"""

from .app import create_app

__all__ = ["create_app"]
