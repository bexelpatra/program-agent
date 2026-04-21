"""/api/notebook — personal vocabulary CRUD."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field

from src import llm_cache, notebook_store
from src.notebook_store import normalize_term
from src.ollama_client import (
    _resolve_model,
    _resolve_prompt_version,
    lookup_term,
)

from ..deps import get_es, get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/notebook", tags=["notebook"])


VALID_SORTS = {"last_added", "added_count", "last_viewed", "first_added", "view_count", "term"}


class NotebookAddRequest(BaseModel):
    term: str = Field(..., min_length=1)
    context: Optional[str] = None
    source_episode_id: Optional[str] = None
    sentence_index: Optional[int] = None


@router.get("")
async def list_entries(
    request: Request,
    sort: str = Query("last_added"),
    term_type: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    es=Depends(get_es),
) -> List[Dict[str, Any]]:
    if sort not in VALID_SORTS:
        raise HTTPException(status_code=400, detail=f"invalid sort '{sort}'")

    filter_: Dict[str, Any] = {}
    if term_type:
        filter_["term_type"] = term_type

    entries = notebook_store.list_notebook(filter=filter_ or None, sort=sort, es=es)

    if q:
        needle = q.strip().lower()
        if needle:
            entries = [
                e
                for e in entries
                if needle in (e.get("term") or "").lower()
                or needle in (e.get("explanation_en") or "").lower()
            ]
    return entries


@router.post("")
async def add_entry(
    payload: NotebookAddRequest,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    settings = get_settings(request)
    model = _resolve_model(settings)
    prompt_version = _resolve_prompt_version(settings)

    # 1) Try cache first, fall back to live ollama call.
    cached = llm_cache.get_cached(payload.term, model, prompt_version, es=es)
    if cached:
        lookup = cached
    else:
        try:
            lookup = await lookup_term(payload.term, payload.context, settings, es=es)
        except Exception as exc:
            logger.exception("lookup_term failed during notebook add for %r", payload.term)
            raise HTTPException(status_code=503, detail=f"lookup failed: {exc}")

    # 2) Upsert into notebook store.
    entry_payload = {
        "term_type": lookup.get("term_type", "word"),
        "explanation_en": lookup.get("explanation_en", ""),
        "etymology": lookup.get("etymology") or "",
    }

    source: Optional[Dict[str, Any]] = None
    if payload.source_episode_id:
        source = {
            "episode_id": payload.source_episode_id,
            "sentence_index": int(payload.sentence_index or 0),
            "added_at": datetime.utcnow().isoformat() + "Z",
        }

    try:
        entry = notebook_store.upsert_notebook_entry(
            payload.term,
            payload=entry_payload,
            source=source,
            es=es,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("notebook upsert failed for %r", payload.term)
        raise HTTPException(status_code=503, detail=f"notebook write failed: {exc}")

    return entry


@router.patch("/{term}/viewed")
async def mark_viewed(term: str, request: Request, es=Depends(get_es)) -> Dict[str, Any]:
    normalized = normalize_term(term)
    if not normalized:
        raise HTTPException(status_code=400, detail="empty term")
    updated = notebook_store.mark_viewed(normalized, es=es)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"term {normalized!r} not found")
    return updated


@router.delete("/{term}", status_code=204)
async def delete_entry(term: str, request: Request, es=Depends(get_es)) -> Response:
    normalized = normalize_term(term)
    if not normalized:
        raise HTTPException(status_code=400, detail="empty term")
    ok = notebook_store.delete_notebook_entry(normalized, es=es)
    if not ok:
        raise HTTPException(status_code=404, detail=f"term {normalized!r} not found")
    return Response(status_code=204)
