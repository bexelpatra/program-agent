"""Tests for src.llm_analyzer module.

Covers provider abstraction, expression detection, CEFR classification,
caching, and batch splitting -- all with mocked LLM calls.
"""

import json
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock, patch, mock_open

import pytest

# ---------------------------------------------------------------------------
# Install mock anthropic module before importing the module under test
# ---------------------------------------------------------------------------

_mock_anthropic_module = MagicMock(spec=ModuleType)
_mock_anthropic_module.__name__ = "anthropic"
_mock_anthropic_module.__package__ = "anthropic"
_mock_anthropic_module.Anthropic = MagicMock

if "anthropic" not in sys.modules:
    sys.modules["anthropic"] = _mock_anthropic_module

from src.llm_analyzer import (  # noqa: E402
    _extract_json,
    _make_cache_key,
    _get_cache,
    _set_cache,
    _split_text_into_chunks,
    _merge_expression_results,
    _parse_expression_result,
    AnthropicProvider,
    OllamaProvider,
    get_provider,
    reset_provider,
    detect_expressions,
    detect_expressions_for_episode,
    classify_vocabulary,
    classify_vocabulary_for_episode,
    _CACHE_DIR,
    _LONG_TEXT_WORD_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Reset the provider singleton before and after each test."""
    reset_provider()
    yield
    reset_provider()


@pytest.fixture
def mock_provider():
    """Return a MagicMock that behaves like an LLMProvider."""
    provider = MagicMock()
    provider.generate.return_value = "mock response"
    provider.generate_json.return_value = []
    return provider


@pytest.fixture
def sample_settings():
    return {
        "llm": {
            "provider": "ollama",
            "ollama": {
                "model": "test-model",
                "base_url": "http://localhost:11434",
                "batch_size": 5,
            },
            "anthropic": {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 4096,
                "batch_size": 10,
            },
        }
    }


@pytest.fixture
def fake_project_root(tmp_path):
    """Create a fake project root with transcript and cache directories."""
    (tmp_path / "data" / "transcripts").mkdir(parents=True)
    (tmp_path / "data" / "cache" / "llm").mkdir(parents=True)
    return tmp_path


def _write_transcript(fake_root, episode_id, data):
    """Helper to write a transcript file into the fake project root."""
    path = fake_root / "data" / "transcripts" / f"{episode_id}_official.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ===================================================================
# _extract_json
# ===================================================================


class TestExtractJson:
    def test_fenced_json_block(self):
        text = 'Some text\n```json\n{"key": "value"}\n```\nMore text'
        result = _extract_json(text)
        assert result == {"key": "value"}

    def test_fenced_json_array(self):
        text = '```json\n[{"a": 1}]\n```'
        result = _extract_json(text)
        assert result == [{"a": 1}]

    def test_plain_json_text(self):
        text = '{"hello": "world"}'
        result = _extract_json(text)
        assert result == {"hello": "world"}

    def test_parse_failure_raises_value_error(self):
        with pytest.raises(ValueError, match="Failed to parse JSON"):
            _extract_json("this is not json at all")

    def test_fenced_block_invalid_falls_through_to_whole_text(self):
        text = '```json\n{invalid}\n```\n{"fallback": true}'
        with pytest.raises(ValueError):
            _extract_json(text)


# ===================================================================
# AnthropicProvider
# ===================================================================


class TestAnthropicProvider:
    def test_creation_requires_api_key(self, sample_settings):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(EnvironmentError, match="ANTHROPIC_API_KEY"):
                AnthropicProvider(sample_settings)

    def test_creation_and_generate(self, sample_settings):
        mock_client = MagicMock()
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "Hello world"
        mock_response = MagicMock()
        mock_response.content = [mock_block]
        mock_client.messages.create.return_value = mock_response

        # Patch the anthropic module in sys.modules so that `import anthropic`
        # inside __init__ picks up our mock.
        mock_anth = MagicMock()
        mock_anth.Anthropic.return_value = mock_client

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch.dict("sys.modules", {"anthropic": mock_anth}):
                provider = AnthropicProvider(sample_settings)
                result = provider.generate("test prompt", system="sys")

        assert result == "Hello world"
        mock_client.messages.create.assert_called_once()
        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["system"] == "sys"
        assert call_kwargs["messages"] == [{"role": "user", "content": "test prompt"}]

    def test_generate_without_system(self, sample_settings):
        mock_client = MagicMock()
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "response"
        mock_response = MagicMock()
        mock_response.content = [mock_block]
        mock_client.messages.create.return_value = mock_response

        mock_anth = MagicMock()
        mock_anth.Anthropic.return_value = mock_client

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch.dict("sys.modules", {"anthropic": mock_anth}):
                provider = AnthropicProvider(sample_settings)
                provider.generate("test prompt")

        call_kwargs = mock_client.messages.create.call_args[1]
        assert "system" not in call_kwargs


# ===================================================================
# OllamaProvider
# ===================================================================


class TestOllamaProvider:
    def test_creation(self, sample_settings):
        provider = OllamaProvider(sample_settings)
        assert provider.model == "test-model"
        assert provider.base_url == "http://localhost:11434"

    def test_generate(self, sample_settings):
        provider = OllamaProvider(sample_settings)
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"response": "ollama says hello"}
        mock_resp.raise_for_status = MagicMock()

        with patch(
            "src.llm_analyzer.http_requests.post", return_value=mock_resp
        ) as mock_post:
            result = provider.generate("test prompt", system="sys prompt")

        assert result == "ollama says hello"
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "test-model",
                "prompt": "test prompt",
                "stream": False,
                "system": "sys prompt",
            },
            timeout=120,
        )

    def test_generate_without_system(self, sample_settings):
        provider = OllamaProvider(sample_settings)
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"response": "hi"}
        mock_resp.raise_for_status = MagicMock()

        with patch(
            "src.llm_analyzer.http_requests.post", return_value=mock_resp
        ) as mock_post:
            provider.generate("prompt only")

        payload = mock_post.call_args[1]["json"]
        assert "system" not in payload


# ===================================================================
# get_provider / reset_provider
# ===================================================================


class TestGetProvider:
    def test_get_ollama_provider(self, sample_settings):
        provider = get_provider(sample_settings)
        assert isinstance(provider, OllamaProvider)

    def test_get_anthropic_provider(self, sample_settings):
        sample_settings["llm"]["provider"] = "anthropic"
        mock_client = MagicMock()
        mock_anth = MagicMock()
        mock_anth.Anthropic.return_value = mock_client

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            with patch.dict("sys.modules", {"anthropic": mock_anth}):
                provider = get_provider(sample_settings)
        assert isinstance(provider, AnthropicProvider)

    def test_singleton_caching(self, sample_settings):
        p1 = get_provider(sample_settings)
        p2 = get_provider(sample_settings)
        assert p1 is p2

    def test_unknown_provider_raises(self, sample_settings):
        sample_settings["llm"]["provider"] = "gpt-magic"
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            get_provider(sample_settings)

    def test_reset_provider(self, sample_settings):
        p1 = get_provider(sample_settings)
        reset_provider()
        p2 = get_provider(sample_settings)
        assert p1 is not p2


# ===================================================================
# Caching
# ===================================================================


class TestCaching:
    def test_make_cache_key_same_input(self):
        k1 = _make_cache_key("expr", "hello world")
        k2 = _make_cache_key("expr", "hello world")
        assert k1 == k2

    def test_make_cache_key_different_input(self):
        k1 = _make_cache_key("expr", "hello")
        k2 = _make_cache_key("expr", "world")
        assert k1 != k2

    def test_make_cache_key_different_prefix(self):
        k1 = _make_cache_key("expr", "hello")
        k2 = _make_cache_key("vocab", "hello")
        assert k1 != k2

    def test_get_set_cache(self, tmp_path):
        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            data = [{"phrase": "kick the bucket"}]
            key = _make_cache_key("test", "content")
            _set_cache(key, data)
            result = _get_cache(key)
            assert result == data

    def test_get_cache_miss(self, tmp_path):
        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            result = _get_cache("nonexistent_key")
            assert result is None

    def test_get_cache_corrupt_file(self, tmp_path):
        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            key = "corrupt_key"
            path = tmp_path / f"{key}.json"
            path.write_text("not valid json {{{", encoding="utf-8")
            result = _get_cache(key)
            assert result is None

    def test_detect_expressions_uses_cache(self, tmp_path, mock_provider):
        """When cache hits, LLM should NOT be called."""
        cached_data = [{"phrase": "cached expression"}]
        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            key = _make_cache_key("expressions", "some text")
            _set_cache(key, cached_data)

            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                result = detect_expressions("some text", settings={})

        assert result == cached_data
        mock_provider.generate_json.assert_not_called()


# ===================================================================
# Text batching
# ===================================================================


class TestBatching:
    def test_split_short_text(self):
        text = "Hello world. This is short."
        chunks = _split_text_into_chunks(text, max_words=100)
        assert len(chunks) == 1

    def test_split_long_text(self):
        sentences = ["Sentence number %d is here." % i for i in range(200)]
        text = " ".join(sentences)
        chunks = _split_text_into_chunks(text, max_words=50)
        assert len(chunks) > 1
        total_words = sum(len(c.split()) for c in chunks)
        assert total_words == len(text.split())

    def test_merge_expression_results_dedup(self):
        results_list = [
            [{"phrase": "kick the bucket"}, {"phrase": "pull strings"}],
            [{"phrase": "Kick The Bucket"}, {"phrase": "break the ice"}],
        ]
        merged = _merge_expression_results(results_list)
        phrases = [r["phrase"] for r in merged]
        assert len(merged) == 3
        assert "kick the bucket" in [p.lower() for p in phrases]
        assert "pull strings" in [p.lower() for p in phrases]
        assert "break the ice" in [p.lower() for p in phrases]

    def test_detect_expressions_splits_long_text(self, tmp_path, mock_provider):
        """Text over threshold should be split into chunks."""
        # Build text with sentence boundaries so _split_text_into_chunks can split
        sentences = [
            "This is sentence number %d." % i
            for i in range(_LONG_TEXT_WORD_THRESHOLD // 5 + 50)
        ]
        long_text = " ".join(sentences)
        assert len(long_text.split()) > _LONG_TEXT_WORD_THRESHOLD

        mock_provider.generate_json.return_value = [{"phrase": "test expr"}]

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                result = detect_expressions(long_text, settings={})

        assert mock_provider.generate_json.call_count > 1
        assert len(result) >= 1


# ===================================================================
# _parse_expression_result
# ===================================================================


class TestParseExpressionResult:
    def test_list_input(self):
        data = [{"phrase": "a"}]
        assert _parse_expression_result(data) == data

    def test_dict_wrapper_expressions(self):
        data = {"expressions": [{"phrase": "a"}]}
        assert _parse_expression_result(data) == [{"phrase": "a"}]

    def test_dict_wrapper_results(self):
        data = {"results": [{"phrase": "a"}]}
        assert _parse_expression_result(data) == [{"phrase": "a"}]

    def test_dict_single_phrase(self):
        data = {"phrase": "kick the bucket", "type": "idiom"}
        assert _parse_expression_result(data) == [data]

    def test_empty_list(self):
        assert _parse_expression_result([]) == []

    def test_unrecognised_structure(self):
        assert _parse_expression_result("something") == []


# ===================================================================
# detect_expressions
# ===================================================================


class TestDetectExpressions:
    def test_normal_result(self, tmp_path, mock_provider):
        expr_list = [
            {"phrase": "kick the bucket", "type": "idiom", "definition_en": "to die"},
        ]
        mock_provider.generate_json.return_value = expr_list

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                result = detect_expressions("He kicked the bucket.", settings={})

        assert len(result) == 1
        assert result[0]["phrase"] == "kick the bucket"

    def test_dict_wrapper_result(self, tmp_path, mock_provider):
        mock_provider.generate_json.return_value = {
            "expressions": [{"phrase": "break the ice"}]
        }

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                result = detect_expressions("Let's break the ice.", settings={})

        assert len(result) == 1
        assert result[0]["phrase"] == "break the ice"

    def test_empty_result(self, tmp_path, mock_provider):
        mock_provider.generate_json.return_value = []

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                result = detect_expressions("Simple text.", settings={})

        assert result == []


# ===================================================================
# detect_expressions_for_episode
# ===================================================================


def _patch_project_root(target_module, fake_root):
    """Return a patch context that makes Path(__file__).resolve().parent.parent
    point to fake_root inside the target module.

    The source code does:
        project_root = Path(__file__).resolve().parent.parent

    We patch the module-level __file__ so that the resolved path yields
    fake_root as the grandparent.
    """
    fake_file = str(fake_root / "src" / "llm_analyzer.py")
    return patch(f"{target_module}.__file__", fake_file, create=True)


class TestDetectExpressionsForEpisode:
    def test_loads_transcript_and_returns_expressions(
        self, fake_project_root, mock_provider
    ):
        transcript = {
            "episode_id": "ep001",
            "full_text": "He kicked the bucket.",
            "sentences": [],
        }
        _write_transcript(fake_project_root, "ep001", transcript)

        mock_provider.generate_json.return_value = [
            {
                "phrase": "kick the bucket",
                "type": "idiom",
                "definition_en": "to die",
                "definition_ko": "죽다",
                "etymology": "origin",
                "difficulty": "B2",
            }
        ]

        cache_dir = fake_project_root / "data" / "cache" / "llm"
        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with _patch_project_root("src.llm_analyzer", fake_project_root):
                    result = detect_expressions_for_episode("ep001", settings={})

        assert len(result) == 1
        assert result[0].phrase == "kick the bucket"
        assert result[0].type == "idiom"
        assert result[0].episodes == ["ep001"]

    def test_type_normalization(self, fake_project_root, mock_provider):
        transcript = {"full_text": "She gave up.", "sentences": []}
        _write_transcript(fake_project_root, "ep002", transcript)

        mock_provider.generate_json.return_value = [
            {
                "phrase": "give up",
                "type": "phrasal verb",
                "definition_en": "stop trying",
                "definition_ko": "포기하다",
                "etymology": "",
                "difficulty": "A2",
            }
        ]

        cache_dir = fake_project_root / "data" / "cache" / "llm"
        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with _patch_project_root("src.llm_analyzer", fake_project_root):
                    result = detect_expressions_for_episode("ep002", settings={})

        assert result[0].type == "phrasal_verb"

    def test_unknown_type_defaults_to_collocation(
        self, fake_project_root, mock_provider
    ):
        transcript = {"full_text": "text", "sentences": []}
        _write_transcript(fake_project_root, "ep003", transcript)

        mock_provider.generate_json.return_value = [
            {"phrase": "heavy rain", "type": "something_unknown"}
        ]

        cache_dir = fake_project_root / "data" / "cache" / "llm"
        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with _patch_project_root("src.llm_analyzer", fake_project_root):
                    result = detect_expressions_for_episode("ep003", settings={})

        assert result[0].type == "collocation"

    def test_transcript_as_string(self, fake_project_root, mock_provider):
        """When transcript JSON is a bare string instead of a dict."""
        _write_transcript(fake_project_root, "ep004", "plain text transcript")
        mock_provider.generate_json.return_value = []

        cache_dir = fake_project_root / "data" / "cache" / "llm"
        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with _patch_project_root("src.llm_analyzer", fake_project_root):
                    result = detect_expressions_for_episode("ep004", settings={})

        assert result == []
        mock_provider.generate_json.assert_called_once()


# ===================================================================
# classify_vocabulary
# ===================================================================


class TestClassifyVocabulary:
    def test_empty_words(self):
        result = classify_vocabulary([], "some text", settings={})
        assert result == []

    def test_normal_classification(self, tmp_path, mock_provider):
        mock_provider.generate_json.return_value = [
            {
                "word": "cat",
                "difficulty": "A1",
                "definition_en": "feline",
                "definition_ko": "고양이",
            },
        ]

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 10}}}

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    result = classify_vocabulary(
                        ["cat"], "The cat sat.", settings=settings
                    )

        assert len(result) == 1
        assert result[0]["word"] == "cat"
        assert result[0]["difficulty"] == "A1"

    def test_batch_splitting(self, tmp_path, mock_provider):
        """Words list larger than batch_size should produce multiple LLM calls."""
        words = [f"word{i}" for i in range(12)]
        mock_provider.generate_json.return_value = [
            {"word": w, "difficulty": "B1", "definition_en": "", "definition_ko": ""}
            for w in words[:5]
        ]

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 5}}}

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    result = classify_vocabulary(
                        words, "context text", settings=settings
                    )

        # With 12 words and batch_size=5, should be 3 calls
        assert mock_provider.generate_json.call_count == 3

    def test_json_parse_failure_fallback(self, tmp_path, mock_provider):
        """On JSON parse failure, empty fields should be returned for each word."""
        mock_provider.generate_json.side_effect = ValueError("parse error")

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 10}}}

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    result = classify_vocabulary(
                        ["hello", "world"], "text", settings=settings
                    )

        assert len(result) == 2
        assert result[0]["word"] == "hello"
        assert result[0]["difficulty"] == ""
        assert result[1]["word"] == "world"

    def test_dict_wrapper_response(self, tmp_path, mock_provider):
        """LLM may return {words: [...]} instead of a plain list."""
        mock_provider.generate_json.return_value = {
            "words": [
                {
                    "word": "test",
                    "difficulty": "A2",
                    "definition_en": "exam",
                    "definition_ko": "시험",
                }
            ]
        }

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 10}}}

        with patch("src.llm_analyzer._CACHE_DIR", tmp_path):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    result = classify_vocabulary(
                        ["test"], "Take a test.", settings=settings
                    )

        assert len(result) == 1
        assert result[0]["word"] == "test"


# ===================================================================
# classify_vocabulary_for_episode
# ===================================================================


class TestClassifyVocabularyForEpisode:
    def test_empty_vocabulary(self):
        result = classify_vocabulary_for_episode("ep001", [], settings={})
        assert result == []

    def test_transcript_not_found(self, fake_project_root):
        vocab = [{"word": "hello"}]
        # No transcript file written, so it won't exist
        with _patch_project_root("src.llm_analyzer", fake_project_root):
            result = classify_vocabulary_for_episode("missing_ep", vocab, settings={})
        assert result == vocab

    def test_normal_flow(self, fake_project_root, mock_provider):
        transcript = {"full_text": "The cat is fast.", "sentences": []}
        _write_transcript(fake_project_root, "ep001", transcript)
        vocab = [{"word": "cat"}, {"word": "fast"}]

        mock_provider.generate_json.return_value = [
            {
                "word": "cat",
                "difficulty": "A1",
                "definition_en": "feline",
                "definition_ko": "고양이",
            },
            {
                "word": "fast",
                "difficulty": "A2",
                "definition_en": "quick",
                "definition_ko": "빠른",
            },
        ]

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 10}}}
        cache_dir = fake_project_root / "data" / "cache" / "llm"

        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    with _patch_project_root("src.llm_analyzer", fake_project_root):
                        result = classify_vocabulary_for_episode(
                            "ep001", vocab, settings=settings
                        )

        assert len(result) == 2
        assert result[0]["difficulty"] == "A1"
        assert result[0]["definition_ko"] == "고양이"
        assert result[1]["difficulty"] == "A2"

    def test_vocab_with_object_items(self, fake_project_root, mock_provider):
        """Vocabulary items can be objects with .word attribute."""
        transcript = {"full_text": "Hello world.", "sentences": []}
        _write_transcript(fake_project_root, "ep001", transcript)

        class VocabItem:
            def __init__(self, word):
                self.word = word

        vocab = [VocabItem("hello")]

        mock_provider.generate_json.return_value = [
            {
                "word": "hello",
                "difficulty": "A1",
                "definition_en": "greeting",
                "definition_ko": "안녕",
            },
        ]

        settings = {"llm": {"provider": "ollama", "ollama": {"batch_size": 10}}}
        cache_dir = fake_project_root / "data" / "cache" / "llm"

        with patch("src.llm_analyzer._CACHE_DIR", cache_dir):
            with patch("src.llm_analyzer.get_provider", return_value=mock_provider):
                with patch("src.llm_analyzer.load_settings", return_value=settings):
                    with _patch_project_root("src.llm_analyzer", fake_project_root):
                        result = classify_vocabulary_for_episode(
                            "ep001", vocab, settings=settings
                        )

        assert len(result) == 1
        assert result[0]["difficulty"] == "A1"
