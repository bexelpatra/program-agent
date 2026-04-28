"""LLM (Ollama) response cache backed by the ``abc-llm-cache`` ES index.

Cache key is ``sha1(term|model|prompt_version)``; it is used as the ES
document ``_id`` so lookups are O(1).
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict, Optional

from .es_client import get_client, get_index_name, load_settings
from .notebook_store import normalize_term


INDEX_KEY = "llm_cache"


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _resolve_index() -> str:
    return get_index_name(INDEX_KEY, settings=load_settings())


def make_cache_key(term: str, model: str, prompt_version: str) -> str:
    """Compute the deterministic sha1 hex cache key for a lookup."""
    normalized = normalize_term(term)
    payload = f"{normalized}|{model}|{prompt_version}".encode("utf-8")
    return hashlib.sha1(payload).hexdigest()


def get_cached(
    term: str,
    model: str,
    prompt_version: str,
    es=None,
) -> Optional[Dict[str, Any]]:
    """Return the cached ``response`` dict, or None on miss/error."""
    key = make_cache_key(term, model, prompt_version)
    client = es or get_client()
    index = _resolve_index()
    try:
        if not client.exists(index=index, id=key):
            return None
        src = client.get(index=index, id=key)["_source"]
        return src.get("response")
    except Exception:
        return None


def set_cached(
    term: str,
    model: str,
    prompt_version: str,
    response: Dict[str, Any],
    es=None,
) -> None:
    """Store ``response`` in the cache for the given (term, model, version)."""
    key = make_cache_key(term, model, prompt_version)
    client = es or get_client()
    index = _resolve_index()
    doc = {
        "cache_key": key,
        "term": normalize_term(term),
        "model": model,
        "prompt_version": prompt_version,
        "response": response or {},
        "created_at": _now_iso(),
    }
    try:
        client.index(index=index, id=key, document=doc, refresh="wait_for")
    except Exception:
        # Cache is best-effort; never propagate failures.
        return
