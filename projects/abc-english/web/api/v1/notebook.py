"""/api/v1/notebook — per-entry user notes for the mobile app.

Differs from the v0 :mod:`web.api.notebook` (term-keyed, ollama-enriched) in
that each doc is a user-authored note with its own UUID and ``last_modified``
timestamp for offline sync. Storage lives in
:mod:`src.notebook_v1_store`.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, Field

from src import notebook_v1_store

from ...deps import get_es

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notebook", tags=["v1", "notebook"])


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------


class NotebookEntryIn(BaseModel):
    word: str = Field(..., min_length=1)
    context: Optional[str] = ""
    episode_id: Optional[str] = ""
    sentence_index: Optional[int] = None
    meaning: Optional[str] = ""
    note: Optional[str] = ""


class NotebookEntryPatch(BaseModel):
    word: Optional[str] = None
    context: Optional[str] = None
    episode_id: Optional[str] = None
    sentence_index: Optional[int] = None
    meaning: Optional[str] = None
    note: Optional[str] = None


class SyncChange(BaseModel):
    id: Optional[str] = None
    op: Literal["upsert", "delete"]
    payload: Optional[Dict[str, Any]] = None
    client_last_modified: Optional[str] = None


class SyncRequest(BaseModel):
    changes: List[SyncChange] = Field(default_factory=list)


class SyncResult(BaseModel):
    id: Optional[str]
    status: Literal["applied", "server_wins", "not_found", "error"]
    server_last_modified: Optional[str] = None
    detail: Optional[str] = None


# ---------------------------------------------------------------------------
# CRUD endpoints
# ---------------------------------------------------------------------------


@router.get("")
async def list_notebook(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=200),
    since_modified: Optional[str] = Query(None),
    es=Depends(get_es),
) -> Dict[str, Any]:
    entries, total = notebook_v1_store.list_entries(
        since_modified=since_modified,
        page=page,
        size=size,
        es=es,
    )
    return {"entries": entries, "total": total, "page": page, "size": size}


@router.post("", status_code=201)
async def create_notebook(
    payload: NotebookEntryIn,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    try:
        return notebook_v1_store.create_entry(payload.model_dump(), es=es)
    except Exception as exc:
        logger.exception("v1 notebook create failed")
        raise HTTPException(status_code=503, detail=f"notebook write failed: {exc}")


@router.patch("/{entry_id}")
async def patch_notebook(
    entry_id: str,
    payload: NotebookEntryPatch,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    # Drop unset (None) fields so we don't overwrite with nulls.
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        updated = notebook_v1_store.patch_entry(entry_id, updates, es=es)
    except Exception as exc:
        logger.exception("v1 notebook patch failed")
        raise HTTPException(status_code=503, detail=f"notebook write failed: {exc}")
    if updated is None:
        raise HTTPException(status_code=404, detail="entry not found")
    return updated


@router.delete("/{entry_id}", status_code=204)
async def delete_notebook(
    entry_id: str,
    request: Request,
    es=Depends(get_es),
) -> Response:
    try:
        ok = notebook_v1_store.delete_entry(entry_id, es=es)
    except Exception as exc:
        logger.exception("v1 notebook delete failed")
        raise HTTPException(status_code=503, detail=f"notebook delete failed: {exc}")
    if not ok:
        raise HTTPException(status_code=404, detail="entry not found")
    return Response(status_code=204)


# ---------------------------------------------------------------------------
# Sync endpoint (TASK-107)
# ---------------------------------------------------------------------------


def _apply_change(change: SyncChange, es) -> Dict[str, Any]:
    if change.op == "delete":
        if not change.id:
            return {"id": None, "status": "error", "detail": "delete requires id"}
        ok = notebook_v1_store.delete_entry(change.id, es=es)
        return {
            "id": change.id,
            "status": "applied" if ok else "not_found",
            "server_last_modified": None,
        }

    # upsert: need at least an id + payload. If no id, create a new entry
    # (treated as server-generated id, always applied).
    payload = change.payload or {}
    client_mtime = change.client_last_modified or ""

    if not change.id:
        doc = notebook_v1_store.create_entry(payload, es=es)
        return {
            "id": doc.get("id"),
            "status": "applied",
            "server_last_modified": doc.get("last_modified"),
        }

    status, doc = notebook_v1_store.upsert_with_id(
        change.id,
        payload,
        client_last_modified=client_mtime,
        es=es,
    )
    return {
        "id": change.id,
        "status": status,
        "server_last_modified": doc.get("last_modified"),
    }


@router.post("/sync")
async def sync_notebook(
    payload: SyncRequest,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    """Best-effort batch upsert/delete with last-write-wins semantics."""
    results: List[Dict[str, Any]] = []
    for change in payload.changes:
        try:
            results.append(_apply_change(change, es))
        except Exception as exc:
            logger.exception("sync change failed: %r", change)
            results.append(
                {
                    "id": change.id,
                    "status": "error",
                    "detail": str(exc),
                }
            )
    return {"results": results}
