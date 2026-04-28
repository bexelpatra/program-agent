"""/api/v1/lookup — GET-based term lookup delegating to the v0 handler.

The v0 endpoint is POST-only (body: ``{term, context?}``). The v1 spec asks
for GET with ``word``/``context`` query params for app-friendliness. Internally
we re-use :func:`web.api.lookup.post_lookup` by constructing the same
``LookupRequest`` so the ollama + cache path stays DRY.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query, Request

from ...deps import get_es
from ..lookup import LookupRequest, post_lookup

router = APIRouter(prefix="/lookup", tags=["v1", "lookup"])


@router.get("")
async def lookup_v1(
    request: Request,
    word: str = Query(..., min_length=1),
    context: Optional[str] = Query(None),
    use_cache: bool = Query(True),
    es=Depends(get_es),
) -> Dict[str, Any]:
    """Delegate to the v0 POST handler with a synthesised payload."""
    payload = LookupRequest(term=word, context=context, use_cache=use_cache)
    return await post_lookup(payload, request, es=es)
