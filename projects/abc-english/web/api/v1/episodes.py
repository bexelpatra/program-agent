"""/api/v1/episodes — versioned episode list + detail.

The v1 contract adds pagination (``page``/``size``), an optional
``since_modified`` ISO8601 filter, and an envelope response
(``{episodes, total, page, size}``) instead of the bare list returned by v0.

Business logic (ES queries) lives in :mod:`web.api.episodes`; this module is a
thin presentation layer.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from ...deps import get_es, get_index

# ISO8601 date or datetime (optional ``T``/``Z``/offset). FastAPI runs this
# regex before binding ``since_modified``; malformed values therefore trigger
# the framework's default 422 response instead of a custom 400.
_ISO8601_REGEX = (
    r"^\d{4}-\d{2}-\d{2}"
    r"(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?)?$"
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/episodes", tags=["v1", "episodes"])


# Fields exposed in the v1 episode list response.
_LIST_FIELDS = (
    "episode_id",
    "title",
    "published_date",
    "duration_seconds",
    "avg_wer",
)

# Additional fields exposed in the v1 episode detail response.
_DETAIL_EXTRA_FIELDS = (
    "description",
    "url",
    "audio_url",
    "has_transcript",
    "sentence_count",
    "word_count",
    "processed_at",
)


def _project_list_source(src: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key in _LIST_FIELDS:
        out[key] = src.get(key)
    # v1 synthetic field: fall back to published_date when last_modified missing.
    out["id"] = src.get("episode_id")
    out["duration"] = src.get("duration_seconds")
    out["last_modified"] = src.get("last_modified") or src.get("processed_at") or src.get("published_date")
    return out


def _project_detail_source(src: Dict[str, Any]) -> Dict[str, Any]:
    out = _project_list_source(src)
    for key in _DETAIL_EXTRA_FIELDS:
        out[key] = src.get(key)
    return out


def _project_sentence(src: Dict[str, Any]) -> Dict[str, Any]:
    start = src.get("start_time")
    end = src.get("end_time")
    return {
        "index": src.get("sentence_index"),
        "text": src.get("official_text") or "",
        # Expose millisecond timestamps for mobile players while preserving the
        # raw seconds field in ``start_time``/``end_time`` for compatibility.
        "start_ms": int((start or 0) * 1000) if start is not None else None,
        "end_ms": int((end or 0) * 1000) if end is not None else None,
        "wer": src.get("wer"),
        "difficulty": src.get("difficulty"),
    }


@router.get("")
async def list_episodes(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=50),
    since_modified: Optional[str] = Query(
        None,
        pattern=_ISO8601_REGEX,
        description="ISO8601 date or datetime; malformed input returns 422.",
    ),
    es=Depends(get_es),
) -> Dict[str, Any]:
    """Paginated episode list sorted by ``published_date`` desc.

    Query params:
        page: 1-indexed page number.
        size: Page size (1..50).
        since_modified: Optional ISO8601 timestamp. Filters to episodes whose
            ``last_modified`` >= the supplied value. Because the existing ES
            mapping does not define ``last_modified`` (see architecture.md
            episode doc), we fall back to ``published_date`` for the range
            filter. TODO: add ``last_modified`` to the mapping when the
            collector starts stamping it.
    """
    index = get_index(request, "episodes")

    must: List[Dict[str, Any]] = [{"match_all": {}}]
    filters: List[Dict[str, Any]] = []
    if since_modified is not None:
        # Regex-validated above; fall back to ``published_date`` per TODO note.
        filters.append({"range": {"published_date": {"gte": since_modified}}})

    query: Dict[str, Any] = (
        {"bool": {"must": must, "filter": filters}} if filters else {"match_all": {}}
    )

    body = {
        "query": query,
        "sort": [{"published_date": {"order": "desc", "missing": "_last"}}],
        "from": (page - 1) * size,
        "size": size,
        "track_total_hits": True,
    }
    try:
        res = es.search(index=index, body=body)
    except NotFoundError:
        return {"episodes": [], "total": 0, "page": page, "size": size}
    except Exception as exc:
        logger.exception("v1 episode list failed")
        raise HTTPException(status_code=503, detail=f"Elasticsearch error: {exc}")

    total_val = res.get("hits", {}).get("total", 0)
    if isinstance(total_val, dict):
        total = int(total_val.get("value", 0))
    else:
        total = int(total_val or 0)

    episodes = [
        _project_list_source(hit.get("_source", {}))
        for hit in res.get("hits", {}).get("hits", [])
    ]
    return {"episodes": episodes, "total": total, "page": page, "size": size}


@router.get("/{episode_id}")
async def get_episode_detail(
    episode_id: str,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    """Episode detail plus ordered sentence list."""
    ep_index = get_index(request, "episodes")
    sent_index = get_index(request, "sentences")

    episode_src: Optional[Dict[str, Any]] = None
    try:
        if es.exists(index=ep_index, id=episode_id):
            episode_src = es.get(index=ep_index, id=episode_id)["_source"]
    except Exception:
        episode_src = None

    if episode_src is None:
        try:
            res = es.search(
                index=ep_index,
                body={"query": {"term": {"episode_id": episode_id}}, "size": 1},
            )
            hits = res["hits"]["hits"]
            if hits:
                episode_src = hits[0]["_source"]
        except Exception:
            episode_src = None

    if episode_src is None:
        raise HTTPException(status_code=404, detail="episode not found")

    try:
        res = es.search(
            index=sent_index,
            body={
                "query": {"term": {"episode_id": episode_id}},
                "sort": [{"sentence_index": {"order": "asc"}}],
                "size": 1000,
            },
        )
        sentences = [_project_sentence(hit["_source"]) for hit in res["hits"]["hits"]]
    except Exception:
        sentences = []

    episode = _project_detail_source(episode_src)
    episode["sentences"] = sentences
    return episode
