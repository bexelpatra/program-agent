"""Elasticsearch bulk loader for ABC English study data.

Loads Episode, Sentence, Vocabulary, and Expression documents into their
respective ES indices using the bulk API for efficient ingestion.
"""

import logging
import re
from typing import Dict, List, Optional

from elasticsearch.helpers import bulk

from .es_client import get_client, get_es_config, get_index_name, load_settings
from .models import Episode, Expression, Sentence, Vocabulary

logger = logging.getLogger(__name__)


def _slug(text: str) -> str:
    """Convert text to a URL-friendly slug (lowercase, spaces to hyphens)."""
    return re.sub(r"\s+", "-", text.strip().lower())


def _bulk_load(
    actions: List[dict],
    settings: Optional[dict] = None,
) -> Dict[str, int]:
    """Execute a bulk load and return loaded/errors counts.

    Args:
        actions: List of bulk action dicts (each with _index, _id, _source).
        settings: Pre-loaded settings dict.

    Returns:
        {"loaded": N, "errors": N}
    """
    if not actions:
        return {"loaded": 0, "errors": 0}

    if settings is None:
        settings = load_settings()

    es = get_client(settings=settings)
    es_conf = get_es_config(settings)
    chunk_size = es_conf.get("bulk_size", 500)

    success, errors = bulk(
        es,
        actions,
        chunk_size=chunk_size,
        raise_on_error=False,
        stats_only=True,
    )

    logger.info("Bulk load complete: %d succeeded, %d errors", success, errors)
    return {"loaded": success, "errors": errors}


def load_episodes(
    episodes: List[Episode], settings: Optional[dict] = None
) -> Dict[str, int]:
    """Load Episode models into the abc-episodes index.

    Args:
        episodes: List of Episode Pydantic models.
        settings: Pre-loaded settings dict.

    Returns:
        {"loaded": N, "errors": N}
    """
    if settings is None:
        settings = load_settings()

    index_name = get_index_name("episodes", settings)
    actions = [
        {
            "_index": index_name,
            "_id": ep.episode_id,
            "_source": ep.model_dump(),
        }
        for ep in episodes
    ]
    return _bulk_load(actions, settings)


def load_sentences(
    sentences: List[Sentence], settings: Optional[dict] = None
) -> Dict[str, int]:
    """Load Sentence models into the abc-sentences index.

    Args:
        sentences: List of Sentence Pydantic models.
        settings: Pre-loaded settings dict.

    Returns:
        {"loaded": N, "errors": N}
    """
    if settings is None:
        settings = load_settings()

    index_name = get_index_name("sentences", settings)

    # Purge any previously-loaded sentences for these episodes so that a
    # finer-grained run doesn't leave stale higher-index docs behind (the
    # ID is {episode_id}_{sentence_index}, so re-loading with fewer
    # sentences would orphan the tail).
    episode_ids = sorted({s.episode_id for s in sentences})
    if episode_ids:
        es = get_client(settings=settings)
        try:
            es.delete_by_query(
                index=index_name,
                query={"terms": {"episode_id": episode_ids}},
                refresh=True,
                conflicts="proceed",
            )
        except Exception as exc:
            logger.warning("delete_by_query for sentences failed: %s", exc)

    actions = [
        {
            "_index": index_name,
            "_id": f"{s.episode_id}_{s.sentence_index}",
            "_source": s.model_dump(),
        }
        for s in sentences
    ]
    return _bulk_load(actions, settings)


def load_vocabulary(
    vocabulary: List[Vocabulary], settings: Optional[dict] = None
) -> Dict[str, int]:
    """Load Vocabulary models into the abc-vocabulary index.

    Args:
        vocabulary: List of Vocabulary Pydantic models.
        settings: Pre-loaded settings dict.

    Returns:
        {"loaded": N, "errors": N}
    """
    if settings is None:
        settings = load_settings()

    index_name = get_index_name("vocabulary", settings)
    actions = [
        {
            "_index": index_name,
            "_id": f"{v.word}_{v.pos}",
            "_source": v.model_dump(),
        }
        for v in vocabulary
    ]
    return _bulk_load(actions, settings)


def load_expressions(
    expressions: List[Expression], settings: Optional[dict] = None
) -> Dict[str, int]:
    """Load Expression models into the abc-expressions index.

    Args:
        expressions: List of Expression Pydantic models.
        settings: Pre-loaded settings dict.

    Returns:
        {"loaded": N, "errors": N}
    """
    if settings is None:
        settings = load_settings()

    index_name = get_index_name("expressions", settings)
    actions = [
        {
            "_index": index_name,
            "_id": _slug(expr.phrase),
            "_source": expr.model_dump(),
        }
        for expr in expressions
    ]
    return _bulk_load(actions, settings)


def load_all(
    episodes: List[Episode],
    sentences: List[Sentence],
    vocabulary: List[Vocabulary],
    expressions: List[Expression],
    settings: Optional[dict] = None,
) -> Dict[str, Dict[str, int]]:
    """Load all data types sequentially and return a combined summary.

    Args:
        episodes: List of Episode models.
        sentences: List of Sentence models.
        vocabulary: List of Vocabulary models.
        expressions: List of Expression models.
        settings: Pre-loaded settings dict.

    Returns:
        Dict with keys 'episodes', 'sentences', 'vocabulary', 'expressions',
        each mapping to {"loaded": N, "errors": N}.
    """
    if settings is None:
        settings = load_settings()

    return {
        "episodes": load_episodes(episodes, settings),
        "sentences": load_sentences(sentences, settings),
        "vocabulary": load_vocabulary(vocabulary, settings),
        "expressions": load_expressions(expressions, settings),
    }
