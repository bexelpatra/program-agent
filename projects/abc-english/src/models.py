"""Data models and Elasticsearch index management.

Defines Pydantic models for the four core data types (Episode, Sentence,
Vocabulary, Expression) and provides functions to create their corresponding
ES indices with explicit mappings.
"""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .es_client import get_client, get_es_config, load_settings


# ---------------------------------------------------------------------------
# Nested / shared models
# ---------------------------------------------------------------------------


class ExampleSentence(BaseModel):
    """An example sentence drawn from a specific episode."""

    episode_id: str
    text: str


# ---------------------------------------------------------------------------
# Core domain models
# ---------------------------------------------------------------------------


class Episode(BaseModel):
    """Represents a single ABC News Daily podcast episode."""

    episode_id: str
    title: str
    description: str = ""
    published_date: datetime
    duration_seconds: int
    url: str
    audio_url: str = ""
    official_transcript: str = ""
    whisper_transcript: str = ""
    has_transcript: bool = True
    sentence_count: int = 0
    word_count: int = 0
    avg_wer: float = 0.0
    processed_at: datetime = Field(default_factory=datetime.utcnow)


class Sentence(BaseModel):
    """A single sentence within an episode, with comparison data."""

    episode_id: str
    sentence_index: int
    official_text: str
    whisper_text: str = ""
    start_time: float = 0.0
    end_time: float = 0.0
    wer: float = 0.0
    listening_difficulty: str = ""
    content_words: List[str] = Field(default_factory=list)
    difficulty: str = ""


class Vocabulary(BaseModel):
    """A vocabulary word extracted from one or more episodes."""

    word: str
    pos: str = ""
    definition_en: str = ""
    definition_ko: str = ""
    difficulty: str = ""
    frequency: int = 0
    episodes: List[str] = Field(default_factory=list)
    example_sentences: List[ExampleSentence] = Field(default_factory=list)


class Expression(BaseModel):
    """An idiom, phrasal verb, or collocation extracted via LLM analysis."""

    phrase: str
    type: Literal["idiom", "phrasal_verb", "collocation"]
    definition_en: str = ""
    definition_ko: str = ""
    etymology: str = ""
    difficulty: str = ""
    frequency: int = 0
    episodes: List[str] = Field(default_factory=list)
    example_sentences: List[ExampleSentence] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# ES index mappings
# ---------------------------------------------------------------------------

EPISODE_MAPPING = {
    "mappings": {
        "properties": {
            "episode_id": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "english"},
            "description": {"type": "text", "analyzer": "english"},
            "published_date": {"type": "date"},
            "duration_seconds": {"type": "integer"},
            "url": {"type": "keyword"},
            "audio_url": {"type": "keyword"},
            "official_transcript": {"type": "text", "analyzer": "english"},
            "whisper_transcript": {"type": "text", "analyzer": "english"},
            "has_transcript": {"type": "boolean"},
            "sentence_count": {"type": "integer"},
            "word_count": {"type": "integer"},
            "avg_wer": {"type": "float"},
            "processed_at": {"type": "date"},
        }
    }
}

SENTENCE_MAPPING = {
    "mappings": {
        "properties": {
            "episode_id": {"type": "keyword"},
            "sentence_index": {"type": "integer"},
            "official_text": {"type": "text", "analyzer": "english"},
            "whisper_text": {"type": "text", "analyzer": "english"},
            "start_time": {"type": "float"},
            "end_time": {"type": "float"},
            "wer": {"type": "float"},
            "listening_difficulty": {"type": "keyword"},
            "content_words": {"type": "keyword"},
            "difficulty": {"type": "keyword"},
        }
    }
}

VOCABULARY_MAPPING = {
    "mappings": {
        "properties": {
            "word": {"type": "keyword"},
            "pos": {"type": "keyword"},
            "definition_en": {"type": "text", "analyzer": "english"},
            "definition_ko": {"type": "text"},
            "difficulty": {"type": "keyword"},
            "frequency": {"type": "integer"},
            "episodes": {"type": "keyword"},
            "example_sentences": {
                "type": "nested",
                "properties": {
                    "episode_id": {"type": "keyword"},
                    "text": {"type": "text", "analyzer": "english"},
                },
            },
        }
    }
}

EXPRESSION_MAPPING = {
    "mappings": {
        "properties": {
            "phrase": {"type": "keyword"},
            "type": {"type": "keyword"},
            "definition_en": {"type": "text", "analyzer": "english"},
            "definition_ko": {"type": "text"},
            "etymology": {"type": "text", "analyzer": "english"},
            "difficulty": {"type": "keyword"},
            "frequency": {"type": "integer"},
            "episodes": {"type": "keyword"},
            "example_sentences": {
                "type": "nested",
                "properties": {
                    "episode_id": {"type": "keyword"},
                    "text": {"type": "text", "analyzer": "english"},
                },
            },
        }
    }
}

# Map logical index keys (matching settings.yaml) to their mappings.
INDEX_MAPPINGS = {
    "episodes": EPISODE_MAPPING,
    "sentences": SENTENCE_MAPPING,
    "vocabulary": VOCABULARY_MAPPING,
    "expressions": EXPRESSION_MAPPING,
}


# ---------------------------------------------------------------------------
# Index management helpers
# ---------------------------------------------------------------------------


def create_indices(settings: Optional[dict] = None, *, recreate: bool = False) -> dict:
    """Create all four ES indices with their mappings.

    Index names are read from ``settings.yaml`` (elasticsearch.indices section).

    Args:
        settings: Pre-loaded settings dict.  When *None* the default
            config file is loaded automatically.
        recreate: If *True*, delete existing indices before creating them.
            **Use with caution** — this destroys data.

    Returns:
        A dict mapping each logical key to a dict with keys ``index_name``
        and ``created`` (bool indicating whether the index was newly created).
    """
    if settings is None:
        settings = load_settings()

    es = get_client(settings=settings)
    es_conf = get_es_config(settings)
    indices_conf = es_conf.get("indices", {})

    results: dict = {}

    for key, mapping in INDEX_MAPPINGS.items():
        index_name = indices_conf.get(key)
        if index_name is None:
            raise KeyError(
                f"Index key '{key}' not found in settings.yaml elasticsearch.indices"
            )

        if recreate and es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)

        if es.indices.exists(index=index_name):
            results[key] = {"index_name": index_name, "created": False}
        else:
            es.indices.create(index=index_name, body=mapping)
            results[key] = {"index_name": index_name, "created": True}

    return results


def delete_indices(settings: Optional[dict] = None) -> dict:
    """Delete all four ES indices.

    Args:
        settings: Pre-loaded settings dict.

    Returns:
        A dict mapping each logical key to a dict with ``index_name``
        and ``deleted`` (bool).
    """
    if settings is None:
        settings = load_settings()

    es = get_client(settings=settings)
    es_conf = get_es_config(settings)
    indices_conf = es_conf.get("indices", {})

    results: dict = {}

    for key in INDEX_MAPPINGS:
        index_name = indices_conf.get(key)
        if index_name is None:
            continue
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            results[key] = {"index_name": index_name, "deleted": True}
        else:
            results[key] = {"index_name": index_name, "deleted": False}

    return results
