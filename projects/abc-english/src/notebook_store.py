"""User vocabulary notebook store (ES CRUD abstraction).

Wraps Elasticsearch operations for the ``abc-user-vocabulary`` index and
exposes a small set of helper functions used by the web API layer.

The ``term`` field acts as the logical key: it is normalized (trim,
collapse whitespace, lowercase) before being used as the document ``_id``.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from .es_client import get_client, get_index_name, load_settings


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Maximum number of source-episode references retained per notebook entry.
MAX_SOURCE_EPISODES = 20

#: Logical index key (matches settings.yaml elasticsearch.indices.user_vocabulary).
INDEX_KEY = "user_vocabulary"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def normalize_term(s: str) -> str:
    """Normalize a term: strip, collapse whitespace, lowercase.

    Args:
        s: Raw user-supplied term.

    Returns:
        Normalized form suitable for use as the ES document id / lookup key.
    """
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s).strip()).lower()


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _resolve_index(es_settings: Optional[dict] = None) -> str:
    if es_settings is None:
        es_settings = load_settings()
    return get_index_name(INDEX_KEY, settings=es_settings)


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------


def upsert_notebook_entry(
    term: str,
    payload: Dict[str, Any],
    source: Optional[Dict[str, Any]] = None,
    es=None,
) -> Dict[str, Any]:
    """Insert or update a notebook entry keyed by normalized term.

    On existing doc: ``added_count += 1``, append ``source`` to
    ``source_episodes`` (keeping at most ``MAX_SOURCE_EPISODES`` most recent
    entries), and bump ``last_added``.

    On new doc: create with ``added_count=1``, ``view_count=0``,
    ``first_added = last_added = now``.

    Args:
        term: Raw term — will be normalized.
        payload: Initial fields (term_type, explanation_en, etymology, note).
        source: ``{"episode_id": str, "sentence_index": int}`` or None.
        es: ES client (optional; uses singleton when omitted).

    Returns:
        The stored document body.
    """
    key = normalize_term(term)
    if not key:
        raise ValueError("term must be non-empty after normalization")

    client = es or get_client()
    index = _resolve_index()
    now = _now_iso()

    source_entry = None
    if source is not None:
        source_entry = {
            "episode_id": source.get("episode_id", ""),
            "sentence_index": int(source.get("sentence_index", 0) or 0),
            "added_at": source.get("added_at", now),
        }

    existing: Optional[Dict[str, Any]] = None
    try:
        if client.exists(index=index, id=key):
            existing = client.get(index=index, id=key)["_source"]
    except Exception:
        existing = None

    if existing is None:
        doc: Dict[str, Any] = {
            "term": key,
            "term_type": payload.get("term_type", "word"),
            "explanation_en": payload.get("explanation_en", ""),
            "etymology": payload.get("etymology", ""),
            "added_count": 1,
            "view_count": 0,
            "first_added": now,
            "last_added": now,
            "last_viewed": None,
            "source_episodes": [source_entry] if source_entry else [],
            "note": payload.get("note", ""),
        }
    else:
        doc = dict(existing)
        doc["term"] = key
        doc["added_count"] = int(doc.get("added_count", 0)) + 1
        doc["last_added"] = now
        # Allow payload to refresh description fields when provided.
        for field in ("term_type", "explanation_en", "etymology", "note"):
            if payload.get(field):
                doc[field] = payload[field]
        sources: List[Dict[str, Any]] = list(doc.get("source_episodes") or [])
        if source_entry:
            sources.append(source_entry)
        # Retain at most MAX_SOURCE_EPISODES most recent entries.
        if len(sources) > MAX_SOURCE_EPISODES:
            sources = sources[-MAX_SOURCE_EPISODES:]
        doc["source_episodes"] = sources
        # Preserve created metadata.
        doc.setdefault("first_added", existing.get("first_added", now))
        doc.setdefault("view_count", int(existing.get("view_count", 0) or 0))
        doc.setdefault("last_viewed", existing.get("last_viewed"))

    client.index(index=index, id=key, document=doc, refresh="wait_for")
    return doc


def get_notebook_entry(term: str, es=None) -> Optional[Dict[str, Any]]:
    """Fetch a notebook entry by term. Returns None when missing."""
    key = normalize_term(term)
    if not key:
        return None
    client = es or get_client()
    index = _resolve_index()
    try:
        if not client.exists(index=index, id=key):
            return None
        return client.get(index=index, id=key)["_source"]
    except Exception:
        return None


def list_notebook(
    filter: Optional[Dict[str, Any]] = None,
    sort: Optional[str] = None,
    es=None,
    size: int = 500,
) -> List[Dict[str, Any]]:
    """List notebook entries.

    Args:
        filter: Optional ``{"term_type": "..."}`` style filter.
        sort: Field name to sort desc by. Defaults to ``last_added``.
            Supported: ``last_added``, ``first_added``, ``last_viewed``,
            ``added_count``, ``view_count``, ``term``.
        es: ES client.
        size: Max results to return.

    Returns:
        List of _source documents.
    """
    client = es or get_client()
    index = _resolve_index()

    query: Dict[str, Any] = {"match_all": {}}
    if filter:
        must = []
        for k, v in filter.items():
            if v is None or v == "":
                continue
            must.append({"term": {k: v}})
        if must:
            query = {"bool": {"must": must}}

    sort_field = sort or "last_added"
    order = "asc" if sort_field == "term" else "desc"
    body = {
        "query": query,
        "sort": [{sort_field: {"order": order, "missing": "_last"}}],
        "size": size,
    }
    try:
        res = client.search(index=index, body=body)
        return [hit["_source"] for hit in res["hits"]["hits"]]
    except Exception:
        return []


def mark_viewed(term: str, es=None) -> Optional[Dict[str, Any]]:
    """Increment view_count and set last_viewed=now for ``term``."""
    key = normalize_term(term)
    if not key:
        return None
    client = es or get_client()
    index = _resolve_index()
    try:
        if not client.exists(index=index, id=key):
            return None
        now = _now_iso()
        script = {
            "source": (
                "ctx._source.view_count = (ctx._source.view_count == null ? 0 "
                ": ctx._source.view_count) + 1; "
                "ctx._source.last_viewed = params.now;"
            ),
            "lang": "painless",
            "params": {"now": now},
        }
        client.update(index=index, id=key, body={"script": script}, refresh="wait_for")
        return client.get(index=index, id=key)["_source"]
    except Exception:
        return None


def delete_notebook_entry(term: str, es=None) -> bool:
    """Delete an entry by term. Returns True when a doc was deleted."""
    key = normalize_term(term)
    if not key:
        return False
    client = es or get_client()
    index = _resolve_index()
    try:
        if not client.exists(index=index, id=key):
            return False
        client.delete(index=index, id=key, refresh="wait_for")
        return True
    except Exception:
        return False
