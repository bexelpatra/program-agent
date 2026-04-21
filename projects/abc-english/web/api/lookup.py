"""/api/lookup — Ollama-backed term/phrase/idiom explanation (cache-first)."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from src import llm_cache
from src.ollama_client import (
    _resolve_model,
    _resolve_prompt_version,
    lookup_term,
)

from ..deps import get_es, get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/lookup", tags=["lookup"])


class LookupRequest(BaseModel):
    term: str = Field(..., min_length=1)
    context: Optional[str] = None
    use_cache: bool = True


@router.post("")
async def post_lookup(
    payload: LookupRequest,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    settings = get_settings(request)

    if payload.use_cache:
        model = _resolve_model(settings)
        prompt_version = _resolve_prompt_version(settings)
        cached = llm_cache.get_cached(payload.term, model, prompt_version, es=es)
        if cached:
            return {"source": "cache", **cached}

    try:
        result = await lookup_term(
            payload.term,
            payload.context,
            settings,
            es=es,
        )
    except Exception as exc:
        logger.exception("ollama lookup failed for %r", payload.term)
        raise HTTPException(status_code=503, detail=f"lookup failed: {exc}")

    return {"source": "ollama", **result}
