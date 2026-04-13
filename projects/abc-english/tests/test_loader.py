"""Unit tests for src/loader.py.

All Elasticsearch operations are mocked — no real ES connection is made.
"""

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.loader import (
    _bulk_load,
    _slug,
    load_all,
    load_episodes,
    load_expressions,
    load_sentences,
    load_vocabulary,
)
from src.models import Episode, Expression, ExampleSentence, Sentence, Vocabulary


# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

SETTINGS = {
    "elasticsearch": {
        "host": "localhost",
        "port": 9200,
        "scheme": "http",
        "bulk_size": 500,
        "indices": {
            "episodes": "abc-episodes",
            "sentences": "abc-sentences",
            "vocabulary": "abc-vocabulary",
            "expressions": "abc-expressions",
        },
    }
}


def _make_episode(**overrides) -> Episode:
    defaults = {
        "episode_id": "ep001",
        "title": "Test Episode",
        "description": "A test episode",
        "published_date": datetime(2024, 1, 1),
        "duration_seconds": 900,
        "url": "https://example.com/ep001",
        "audio_url": "https://example.com/ep001.mp3",
    }
    defaults.update(overrides)
    return Episode(**defaults)


def _make_sentence(**overrides) -> Sentence:
    defaults = {
        "episode_id": "ep001",
        "sentence_index": 0,
        "official_text": "Hello world.",
        "whisper_text": "Hello world.",
        "wer": 0.0,
    }
    defaults.update(overrides)
    return Sentence(**defaults)


def _make_vocabulary(**overrides) -> Vocabulary:
    defaults = {
        "word": "hello",
        "pos": "interjection",
        "definition_en": "a greeting",
        "frequency": 5,
        "episodes": ["ep001"],
    }
    defaults.update(overrides)
    return Vocabulary(**defaults)


def _make_expression(**overrides) -> Expression:
    defaults = {
        "phrase": "break the ice",
        "type": "idiom",
        "definition_en": "to initiate conversation",
        "frequency": 3,
        "episodes": ["ep001"],
    }
    defaults.update(overrides)
    return Expression(**defaults)


# ---------------------------------------------------------------------------
# _slug
# ---------------------------------------------------------------------------


class TestSlug:
    def test_basic(self):
        assert _slug("break the ice") == "break-the-ice"

    def test_leading_trailing_whitespace(self):
        assert _slug("  hello world  ") == "hello-world"

    def test_multiple_spaces(self):
        assert _slug("a   b   c") == "a-b-c"

    def test_already_lowercase(self):
        assert _slug("already-slugged") == "already-slugged"

    def test_uppercase(self):
        assert _slug("Hello World") == "hello-world"


# ---------------------------------------------------------------------------
# _bulk_load
# ---------------------------------------------------------------------------


class TestBulkLoad:
    @patch("src.loader.get_client")
    @patch("src.loader.get_es_config")
    @patch("src.loader.bulk")
    def test_basic_load(self, mock_bulk, mock_es_config, mock_get_client):
        mock_es_config.return_value = {"bulk_size": 500}
        mock_get_client.return_value = MagicMock()
        mock_bulk.return_value = (3, 0)

        actions = [{"_index": "test", "_id": "1", "_source": {}}] * 3
        result = _bulk_load(actions, settings=SETTINGS)

        assert result == {"loaded": 3, "errors": 0}
        mock_bulk.assert_called_once()

    @patch("src.loader.get_client")
    @patch("src.loader.get_es_config")
    @patch("src.loader.bulk")
    def test_with_errors(self, mock_bulk, mock_es_config, mock_get_client):
        mock_es_config.return_value = {"bulk_size": 500}
        mock_get_client.return_value = MagicMock()
        mock_bulk.return_value = (2, 1)

        actions = [{"_index": "test", "_id": "1", "_source": {}}] * 3
        result = _bulk_load(actions, settings=SETTINGS)

        assert result == {"loaded": 2, "errors": 1}

    def test_empty_actions(self):
        """Empty action list should return zeros without calling ES."""
        result = _bulk_load([], settings=SETTINGS)
        assert result == {"loaded": 0, "errors": 0}

    @patch("src.loader.get_client")
    @patch("src.loader.get_es_config")
    @patch("src.loader.bulk")
    @patch("src.loader.load_settings")
    def test_loads_settings_when_none(
        self, mock_load_settings, mock_bulk, mock_es_config, mock_get_client
    ):
        mock_load_settings.return_value = SETTINGS
        mock_es_config.return_value = {"bulk_size": 500}
        mock_get_client.return_value = MagicMock()
        mock_bulk.return_value = (1, 0)

        actions = [{"_index": "test", "_id": "1", "_source": {}}]
        result = _bulk_load(actions, settings=None)

        mock_load_settings.assert_called_once()
        assert result == {"loaded": 1, "errors": 0}

    @patch("src.loader.get_client")
    @patch("src.loader.get_es_config")
    @patch("src.loader.bulk")
    def test_bulk_size_from_config(self, mock_bulk, mock_es_config, mock_get_client):
        mock_es_config.return_value = {"bulk_size": 100}
        mock_get_client.return_value = MagicMock()
        mock_bulk.return_value = (1, 0)

        actions = [{"_index": "test", "_id": "1", "_source": {}}]
        _bulk_load(actions, settings=SETTINGS)

        _, kwargs = mock_bulk.call_args
        assert kwargs["chunk_size"] == 100

    @patch("src.loader.get_client")
    @patch("src.loader.get_es_config")
    @patch("src.loader.bulk")
    def test_default_bulk_size(self, mock_bulk, mock_es_config, mock_get_client):
        """When bulk_size is missing from config, default to 500."""
        mock_es_config.return_value = {}
        mock_get_client.return_value = MagicMock()
        mock_bulk.return_value = (1, 0)

        actions = [{"_index": "test", "_id": "1", "_source": {}}]
        _bulk_load(actions, settings=SETTINGS)

        _, kwargs = mock_bulk.call_args
        assert kwargs["chunk_size"] == 500


# ---------------------------------------------------------------------------
# load_episodes
# ---------------------------------------------------------------------------


class TestLoadEpisodes:
    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-episodes")
    def test_creates_correct_actions(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 2, "errors": 0}
        ep1 = _make_episode(episode_id="ep001")
        ep2 = _make_episode(episode_id="ep002")

        result = load_episodes([ep1, ep2], settings=SETTINGS)

        assert result == {"loaded": 2, "errors": 0}
        actions = mock_bulk.call_args[0][0]
        assert len(actions) == 2
        assert actions[0]["_index"] == "abc-episodes"
        assert actions[0]["_id"] == "ep001"
        assert actions[1]["_id"] == "ep002"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-episodes")
    def test_id_is_episode_id(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        ep = _make_episode(episode_id="my-unique-id")

        load_episodes([ep], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        assert actions[0]["_id"] == "my-unique-id"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-episodes")
    def test_empty_list(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 0, "errors": 0}
        result = load_episodes([], settings=SETTINGS)
        assert result == {"loaded": 0, "errors": 0}


# ---------------------------------------------------------------------------
# load_sentences
# ---------------------------------------------------------------------------


class TestLoadSentences:
    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-sentences")
    def test_creates_correct_actions(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 2, "errors": 0}
        s1 = _make_sentence(episode_id="ep001", sentence_index=0)
        s2 = _make_sentence(episode_id="ep001", sentence_index=1)

        result = load_sentences([s1, s2], settings=SETTINGS)

        assert result == {"loaded": 2, "errors": 0}
        actions = mock_bulk.call_args[0][0]
        assert len(actions) == 2
        assert actions[0]["_index"] == "abc-sentences"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-sentences")
    def test_id_format(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        s = _make_sentence(episode_id="ep005", sentence_index=3)

        load_sentences([s], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        assert actions[0]["_id"] == "ep005_3"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-sentences")
    def test_empty_list(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 0, "errors": 0}
        result = load_sentences([], settings=SETTINGS)
        assert result == {"loaded": 0, "errors": 0}


# ---------------------------------------------------------------------------
# load_vocabulary
# ---------------------------------------------------------------------------


class TestLoadVocabulary:
    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-vocabulary")
    def test_creates_correct_actions(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 2, "errors": 0}
        v1 = _make_vocabulary(word="hello", pos="interjection")
        v2 = _make_vocabulary(word="run", pos="verb")

        result = load_vocabulary([v1, v2], settings=SETTINGS)

        assert result == {"loaded": 2, "errors": 0}
        actions = mock_bulk.call_args[0][0]
        assert len(actions) == 2
        assert actions[0]["_index"] == "abc-vocabulary"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-vocabulary")
    def test_id_format(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        v = _make_vocabulary(word="run", pos="verb")

        load_vocabulary([v], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        assert actions[0]["_id"] == "run_verb"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-vocabulary")
    def test_empty_list(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 0, "errors": 0}
        result = load_vocabulary([], settings=SETTINGS)
        assert result == {"loaded": 0, "errors": 0}


# ---------------------------------------------------------------------------
# load_expressions
# ---------------------------------------------------------------------------


class TestLoadExpressions:
    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-expressions")
    def test_creates_correct_actions(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 2, "errors": 0}
        e1 = _make_expression(phrase="break the ice")
        e2 = _make_expression(phrase="piece of cake")

        result = load_expressions([e1, e2], settings=SETTINGS)

        assert result == {"loaded": 2, "errors": 0}
        actions = mock_bulk.call_args[0][0]
        assert len(actions) == 2
        assert actions[0]["_index"] == "abc-expressions"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-expressions")
    def test_id_is_slugified_phrase(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        e = _make_expression(phrase="break the ice")

        load_expressions([e], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        assert actions[0]["_id"] == "break-the-ice"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-expressions")
    def test_slug_with_uppercase(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        e = _make_expression(phrase="Break The Ice")

        load_expressions([e], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        assert actions[0]["_id"] == "break-the-ice"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-expressions")
    def test_empty_list(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 0, "errors": 0}
        result = load_expressions([], settings=SETTINGS)
        assert result == {"loaded": 0, "errors": 0}


# ---------------------------------------------------------------------------
# load_all
# ---------------------------------------------------------------------------


class TestLoadAll:
    @patch("src.loader.load_expressions")
    @patch("src.loader.load_vocabulary")
    @patch("src.loader.load_sentences")
    @patch("src.loader.load_episodes")
    def test_calls_all_four(self, mock_ep, mock_sent, mock_vocab, mock_expr):
        mock_ep.return_value = {"loaded": 1, "errors": 0}
        mock_sent.return_value = {"loaded": 2, "errors": 0}
        mock_vocab.return_value = {"loaded": 3, "errors": 0}
        mock_expr.return_value = {"loaded": 4, "errors": 0}

        episodes = [_make_episode()]
        sentences = [_make_sentence(), _make_sentence(sentence_index=1)]
        vocabulary = [
            _make_vocabulary(),
            _make_vocabulary(word="run", pos="verb"),
            _make_vocabulary(word="go", pos="verb"),
        ]
        expressions = [_make_expression()] * 4

        result = load_all(
            episodes, sentences, vocabulary, expressions, settings=SETTINGS
        )

        assert result["episodes"] == {"loaded": 1, "errors": 0}
        assert result["sentences"] == {"loaded": 2, "errors": 0}
        assert result["vocabulary"] == {"loaded": 3, "errors": 0}
        assert result["expressions"] == {"loaded": 4, "errors": 0}

        mock_ep.assert_called_once_with(episodes, SETTINGS)
        mock_sent.assert_called_once_with(sentences, SETTINGS)
        mock_vocab.assert_called_once_with(vocabulary, SETTINGS)
        mock_expr.assert_called_once_with(expressions, SETTINGS)

    @patch("src.loader.load_expressions")
    @patch("src.loader.load_vocabulary")
    @patch("src.loader.load_sentences")
    @patch("src.loader.load_episodes")
    def test_all_empty(self, mock_ep, mock_sent, mock_vocab, mock_expr):
        mock_ep.return_value = {"loaded": 0, "errors": 0}
        mock_sent.return_value = {"loaded": 0, "errors": 0}
        mock_vocab.return_value = {"loaded": 0, "errors": 0}
        mock_expr.return_value = {"loaded": 0, "errors": 0}

        result = load_all([], [], [], [], settings=SETTINGS)

        assert all(v == {"loaded": 0, "errors": 0} for v in result.values())

    @patch("src.loader.load_expressions")
    @patch("src.loader.load_vocabulary")
    @patch("src.loader.load_sentences")
    @patch("src.loader.load_episodes")
    def test_with_errors(self, mock_ep, mock_sent, mock_vocab, mock_expr):
        mock_ep.return_value = {"loaded": 1, "errors": 0}
        mock_sent.return_value = {"loaded": 5, "errors": 2}
        mock_vocab.return_value = {"loaded": 0, "errors": 3}
        mock_expr.return_value = {"loaded": 1, "errors": 1}

        result = load_all(
            [_make_episode()],
            [_make_sentence()],
            [_make_vocabulary()],
            [_make_expression()],
            settings=SETTINGS,
        )

        assert result["sentences"]["errors"] == 2
        assert result["vocabulary"]["errors"] == 3
        assert result["expressions"]["errors"] == 1

    @patch("src.loader.load_expressions")
    @patch("src.loader.load_vocabulary")
    @patch("src.loader.load_sentences")
    @patch("src.loader.load_episodes")
    @patch("src.loader.load_settings")
    def test_loads_settings_when_none(
        self, mock_load_settings, mock_ep, mock_sent, mock_vocab, mock_expr
    ):
        mock_load_settings.return_value = SETTINGS
        mock_ep.return_value = {"loaded": 0, "errors": 0}
        mock_sent.return_value = {"loaded": 0, "errors": 0}
        mock_vocab.return_value = {"loaded": 0, "errors": 0}
        mock_expr.return_value = {"loaded": 0, "errors": 0}

        load_all([], [], [], [], settings=None)

        mock_load_settings.assert_called_once()

    @patch("src.loader.load_expressions")
    @patch("src.loader.load_vocabulary")
    @patch("src.loader.load_sentences")
    @patch("src.loader.load_episodes")
    def test_returns_all_four_keys(self, mock_ep, mock_sent, mock_vocab, mock_expr):
        for m in (mock_ep, mock_sent, mock_vocab, mock_expr):
            m.return_value = {"loaded": 0, "errors": 0}

        result = load_all([], [], [], [], settings=SETTINGS)

        assert set(result.keys()) == {
            "episodes",
            "sentences",
            "vocabulary",
            "expressions",
        }


# ---------------------------------------------------------------------------
# Integration-like: action construction verification
# ---------------------------------------------------------------------------


class TestActionConstruction:
    """Verify that model_dump() output is correctly placed in _source."""

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-episodes")
    def test_episode_source_contains_model_data(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        ep = _make_episode(title="My Title", episode_id="ep999")

        load_episodes([ep], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        source = actions[0]["_source"]
        assert source["title"] == "My Title"
        assert source["episode_id"] == "ep999"

    @patch("src.loader._bulk_load")
    @patch("src.loader.get_index_name", return_value="abc-vocabulary")
    def test_vocabulary_source_contains_model_data(self, mock_index, mock_bulk):
        mock_bulk.return_value = {"loaded": 1, "errors": 0}
        v = _make_vocabulary(
            word="test",
            pos="noun",
            example_sentences=[
                ExampleSentence(episode_id="ep001", text="This is a test.")
            ],
        )

        load_vocabulary([v], settings=SETTINGS)

        actions = mock_bulk.call_args[0][0]
        source = actions[0]["_source"]
        assert source["word"] == "test"
        assert len(source["example_sentences"]) == 1
        assert source["example_sentences"][0]["text"] == "This is a test."
