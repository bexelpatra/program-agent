"""Notebook store for the /api/v1 mobile-app contract.

The v0 notebook (:mod:`src.notebook_store`) is keyed by *term* and carries
ollama-generated explanation fields. The v1 contract is a simple per-entry
user note — ``{word, context, episode_id, sentence_index, meaning, note}`` —
keyed by an opaque UUID and timestamped with ``created_at`` / ``last_modified``
for offline sync.

To avoid entangling two different domain models, v1 writes to its own index
(``abc-notebook-v1`` by default) rather than the legacy ``abc-user-vocabulary``
index.

Public API:
    ensure_index(es)               -> None
    create_entry(payload, es)      -> dict
    get_entry(entry_id, es)        -> dict | None
    list_entries(...)              -> (list[dict], total)
    patch_entry(entry_id, ..., es) -> dict | None
    delete_entry(entry_id, es)     -> bool
    upsert_with_id(entry_id, ...)  -> dict (used by /sync)
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .es_client import get_client, get_es_config, load_settings


INDEX_KEY = "notebook_v1"
DEFAULT_INDEX_NAME = "abc-notebook-v1"


# Fields editable via POST/PATCH/upsert.
_MUTABLE_FIELDS = (
    "word",
    "context",
    "episode_id",
    "sentence_index",
    "meaning",
    "note",
)


NOTEBOOK_V1_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "word": {"type": "keyword"},
            "context": {"type": "text"},
            "episode_id": {"type": "keyword"},
            "sentence_index": {"type": "integer"},
            "meaning": {"type": "text"},
            "note": {"type": "text"},
            "created_at": {"type": "date"},
            "last_modified": {"type": "date"},
        }
    }
}


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _resolve_index(settings: Optional[Dict[str, Any]] = None) -> str:
    if settings is None:
        settings = load_settings()
    es_conf = get_es_config(settings)
    indices = es_conf.get("indices", {})
    return indices.get(INDEX_KEY, DEFAULT_INDEX_NAME)


def _coerce_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Keep only known mutable fields, defaulting missing strings to ''."""
    out: Dict[str, Any] = {}
    for key in _MUTABLE_FIELDS:
        if key in payload:
            value = payload[key]
            if key == "sentence_index":
                out[key] = int(value) if value is not None else None
            else:
                out[key] = "" if value is None else str(value)
    return out


def ensure_index(es=None, settings: Optional[Dict[str, Any]] = None) -> str:
    """Create the v1 notebook index if it does not exist. Returns its name."""
    client = es or get_client()
    index = _resolve_index(settings)
    try:
        if not client.indices.exists(index=index):
            client.indices.create(index=index, body=NOTEBOOK_V1_MAPPING)
    except Exception:
        # Best-effort — the CRUD paths fall back to 503 if the index is
        # genuinely missing.
        pass
    return index


def create_entry(
    payload: Dict[str, Any],
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a new entry with a server-assigned UUID. Returns the stored doc."""
    client = es or get_client()
    index = ensure_index(client, settings)
    now = _now_iso()
    entry_id = str(uuid.uuid4())
    doc: Dict[str, Any] = {
        "id": entry_id,
        "created_at": now,
        "last_modified": now,
    }
    # Default all mutable fields.
    for key in _MUTABLE_FIELDS:
        doc[key] = "" if key != "sentence_index" else None
    doc.update(_coerce_payload(payload))
    client.index(index=index, id=entry_id, document=doc, refresh="wait_for")
    return doc


def get_entry(
    entry_id: str,
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    if not entry_id:
        return None
    client = es or get_client()
    index = _resolve_index(settings)
    try:
        if not client.exists(index=index, id=entry_id):
            return None
        return client.get(index=index, id=entry_id)["_source"]
    except Exception:
        return None


def list_entries(
    since_modified: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], int]:
    """Paginated list sorted by ``last_modified`` desc."""
    client = es or get_client()
    index = ensure_index(client, settings)

    filters: List[Dict[str, Any]] = []
    if since_modified:
        filters.append({"range": {"last_modified": {"gte": since_modified}}})

    query: Dict[str, Any] = (
        {"bool": {"filter": filters}} if filters else {"match_all": {}}
    )
    body = {
        "query": query,
        "sort": [{"last_modified": {"order": "desc", "missing": "_last"}}],
        "from": max(0, (page - 1) * size),
        "size": size,
        "track_total_hits": True,
    }
    try:
        res = client.search(index=index, body=body)
    except Exception:
        return [], 0

    total_val = res.get("hits", {}).get("total", 0)
    if isinstance(total_val, dict):
        total = int(total_val.get("value", 0))
    else:
        total = int(total_val or 0)
    entries = [hit["_source"] for hit in res.get("hits", {}).get("hits", [])]
    return entries, total


def patch_entry(
    entry_id: str,
    payload: Dict[str, Any],
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Apply a partial update. Returns the updated doc or None when missing."""
    client = es or get_client()
    index = _resolve_index(settings)

    existing = get_entry(entry_id, es=client, settings=settings)
    if existing is None:
        return None

    updates = _coerce_payload(payload)
    if not updates:
        # No-op patch still bumps last_modified for LWW correctness.
        updates = {}
    doc = dict(existing)
    doc.update(updates)
    doc["id"] = entry_id
    doc["last_modified"] = _now_iso()
    doc.setdefault("created_at", existing.get("created_at") or doc["last_modified"])

    client.index(index=index, id=entry_id, document=doc, refresh="wait_for")
    return doc


def delete_entry(
    entry_id: str,
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> bool:
    if not entry_id:
        return False
    client = es or get_client()
    index = _resolve_index(settings)
    try:
        if not client.exists(index=index, id=entry_id):
            return False
        client.delete(index=index, id=entry_id, refresh="wait_for")
        return True
    except Exception:
        return False


def upsert_with_id(
    entry_id: str,
    payload: Dict[str, Any],
    client_last_modified: str,
    es=None,
    settings: Optional[Dict[str, Any]] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Last-write-wins upsert used by /sync.

    Returns a ``(status, doc)`` tuple where ``status`` is one of
    ``"applied"`` (new or client-wins overwrite) or ``"server_wins"`` (no-op
    because the server copy is newer/equal).
    """
    client = es or get_client()
    index = ensure_index(client, settings)
    now = _now_iso()

    existing = get_entry(entry_id, es=client, settings=settings)

    if existing is None:
        doc: Dict[str, Any] = {
            "id": entry_id,
            "created_at": now,
            "last_modified": client_last_modified or now,
        }
        for key in _MUTABLE_FIELDS:
            doc[key] = "" if key != "sentence_index" else None
        doc.update(_coerce_payload(payload))
        client.index(index=index, id=entry_id, document=doc, refresh="wait_for")
        return "applied", doc

    server_mtime = str(existing.get("last_modified") or "")
    if client_last_modified and client_last_modified > server_mtime:
        doc = dict(existing)
        doc.update(_coerce_payload(payload))
        doc["id"] = entry_id
        doc["last_modified"] = client_last_modified
        doc.setdefault("created_at", existing.get("created_at") or now)
        client.index(index=index, id=entry_id, document=doc, refresh="wait_for")
        return "applied", doc

    return "server_wins", existing
