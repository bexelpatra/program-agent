"""/api/episodes routes — list episodes and fetch per-episode sentences."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from elasticsearch import NotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from ..deps import get_es, get_index

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/episodes", tags=["episodes"])


EPISODE_FIELDS = (
    "episode_id",
    "title",
    "published_date",
    "duration_seconds",
    "has_transcript",
    "sentence_count",
    "word_count",
)


def _clean_episode(src: Dict[str, Any]) -> Dict[str, Any]:
    return {k: src.get(k) for k in EPISODE_FIELDS}


def _clean_sentence(src: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sentence_index": src.get("sentence_index"),
        "official_text": src.get("official_text"),
        "start_time": src.get("start_time"),
        "end_time": src.get("end_time"),
        "difficulty": src.get("difficulty"),
        "wer": src.get("wer"),
        "listening_difficulty": src.get("listening_difficulty"),
    }


@router.get("", response_model=None)
async def list_episodes(
    request: Request,
    limit: int = Query(100, ge=1, le=500),
    es=Depends(get_es),
) -> List[Dict[str, Any]]:
    """Return episodes sorted by ``published_date`` desc."""
    index = get_index(request, "episodes")
    body = {
        "query": {"match_all": {}},
        "sort": [{"published_date": {"order": "desc", "missing": "_last"}}],
        "size": limit,
    }
    try:
        res = es.search(index=index, body=body)
    except NotFoundError:
        return []
    except Exception as exc:
        logger.exception("episode list failed")
        raise HTTPException(status_code=503, detail=f"Elasticsearch error: {exc}")

    return [_clean_episode(hit["_source"]) for hit in res["hits"]["hits"]]


@router.get("/{episode_id}")
async def get_episode(
    episode_id: str,
    request: Request,
    es=Depends(get_es),
) -> Dict[str, Any]:
    """Return a single episode plus its sentences ordered by ``sentence_index``."""
    ep_index = get_index(request, "episodes")
    sent_index = get_index(request, "sentences")

    # Primary fetch by _id, with fallback term query on episode_id.
    episode_src: Dict[str, Any] | None = None
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
        raise HTTPException(status_code=404, detail=f"episode {episode_id!r} not found")

    body = {
        "query": {"term": {"episode_id": episode_id}},
        "sort": [{"sentence_index": {"order": "asc"}}],
        "size": 1000,
    }
    try:
        res = es.search(index=sent_index, body=body)
        sentences = [_clean_sentence(hit["_source"]) for hit in res["hits"]["hits"]]
    except Exception:
        sentences = []

    return {"episode": _clean_episode(episode_src), "sentences": sentences}
