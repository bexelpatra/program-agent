"""/api/study/helper — unified flashcard feed from vocabulary + expressions.

Returns a flat list of cards sorted so idioms and harder words come first,
which satisfies the "must include hard words and idioms" requirement while
letting the client page through the rest.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, Request

from ..deps import get_es, get_index

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/study/helper", tags=["study"])


# CEFR rough ordering — higher = harder.
_CEFR_RANK = {"A1": 1, "A2": 2, "B1": 3, "B2": 4, "C1": 5, "C2": 6}

# Bucket mapping for the "difficulty" UI filter.
_HARD = {"B2", "C1", "C2"}
_MEDIUM = {"B1"}
_EASY = {"A1", "A2"}


def _bucket_matches(level: str, bucket: str) -> bool:
    if bucket == "all":
        return True
    if bucket == "hard":
        return level in _HARD
    if bucket == "medium":
        return level in _MEDIUM
    if bucket == "easy":
        return level in _EASY
    return True


def _card_sort_key(card: Dict[str, Any]) -> tuple:
    # Sort: idioms first, then by CEFR desc, then by frequency desc.
    is_idiom = card.get("kind") == "expression" and card.get("type") == "idiom"
    cefr = _CEFR_RANK.get(card.get("difficulty") or "", 0)
    freq = int(card.get("frequency") or 0)
    return (0 if is_idiom else 1, -cefr, -freq)


@router.get("")
def get_helper_cards(
    request: Request,
    type: str = Query("all", pattern="^(all|vocabulary|expression)$"),
    difficulty: str = Query("all", pattern="^(all|hard|medium|easy)$"),
    episode_id: str = Query("", description="Filter to a single episode"),
    limit: int = Query(500, ge=1, le=2000),
) -> List[Dict[str, Any]]:
    es = get_es(request)

    cards: List[Dict[str, Any]] = []

    def _scope(base_query: Dict[str, Any]) -> Dict[str, Any]:
        if not episode_id:
            return base_query
        ep_filter = {"term": {"episodes": episode_id}}
        if "bool" in base_query:
            q = {"bool": dict(base_query["bool"])}
            q["bool"].setdefault("filter", [])
            q["bool"]["filter"] = list(q["bool"]["filter"]) + [ep_filter]
            return q
        return {"bool": {"must": [base_query], "filter": [ep_filter]}}

    if type in ("all", "expression"):
        idx = get_index(request, "expressions")
        res = es.search(index=idx, size=limit, query=_scope({"match_all": {}}))
        for hit in res.get("hits", {}).get("hits", []):
            src = hit.get("_source", {})
            level = (src.get("difficulty") or "").upper()
            if not _bucket_matches(level, difficulty):
                continue
            cards.append(
                {
                    "id": hit.get("_id"),
                    "kind": "expression",
                    "term": src.get("phrase", ""),
                    "type": src.get("type", ""),
                    "definition_en": src.get("definition_en", ""),
                    "definition_ko": src.get("definition_ko", ""),
                    "etymology": src.get("etymology", ""),
                    "examples": src.get("example_sentences") or [],
                    "difficulty": level,
                    "frequency": src.get("frequency", 0),
                    "episodes": src.get("episodes") or [],
                }
            )

    if type in ("all", "vocabulary"):
        idx = get_index(request, "vocabulary")
        # Always exclude empty-difficulty vocab so UI isn't flooded with unlabeled.
        q: Dict[str, Any]
        if difficulty == "all":
            q = {"bool": {"must": [{"exists": {"field": "difficulty"}}],
                          "must_not": [{"term": {"difficulty": ""}}]}}
        else:
            levels = {"hard": list(_HARD), "medium": list(_MEDIUM), "easy": list(_EASY)}[difficulty]
            q = {"terms": {"difficulty": levels}}
        res = es.search(index=idx, size=limit, query=_scope(q),
                        sort=[{"frequency": "desc"}])
        for hit in res.get("hits", {}).get("hits", []):
            src = hit.get("_source", {})
            level = (src.get("difficulty") or "").upper()
            if not _bucket_matches(level, difficulty):
                continue
            cards.append(
                {
                    "id": hit.get("_id"),
                    "kind": "vocabulary",
                    "term": src.get("word", ""),
                    "type": src.get("pos", ""),
                    "definition_en": src.get("definition_en", ""),
                    "definition_ko": src.get("definition_ko", ""),
                    "etymology": "",
                    "examples": src.get("example_sentences") or [],
                    "difficulty": level,
                    "frequency": src.get("frequency", 0),
                    "episodes": src.get("episodes") or [],
                }
            )

    cards.sort(key=_card_sort_key)
    return cards[:limit]
