"""Tests for src/analyzer.py — spaCy NLP vocabulary analysis module.

spaCy is mocked because the model may not be installed in the test
environment.  We build lightweight mock Token / Doc / Span objects that
provide the attributes the production code actually reads.
"""

import json
from pathlib import Path
from types import SimpleNamespace
from typing import List
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Mock helpers — lightweight stand-ins for spaCy objects
# ---------------------------------------------------------------------------


def _make_token(i, text, lemma, pos_, is_space=False):
    """Return a mock token with the attrs analyzer.py reads."""
    tok = SimpleNamespace(
        i=i,
        text=text,
        lemma_=lemma,
        pos_=pos_,
        is_space=is_space,
    )
    # .strip() is called on tok.text
    tok.text = text
    return tok


class _MockSent:
    """Minimal sentence span."""

    def __init__(self, text: str, tokens: list):
        self._text = text
        self._tokens = tokens

    @property
    def text(self):
        return self._text

    def __iter__(self):
        return iter(self._tokens)


class _MockEnt:
    """Minimal entity span."""

    def __init__(self, label_: str, tokens: list):
        self.label_ = label_
        self._tokens = tokens

    def __iter__(self):
        return iter(self._tokens)


class _MockDoc:
    """Minimal Doc that supports iteration, .ents, and .sents."""

    def __init__(self, tokens, ents=None, sents=None):
        self._tokens = tokens
        self.ents = ents or []
        self._sents = sents or []

    @property
    def sents(self):
        return iter(self._sents)

    def __iter__(self):
        return iter(self._tokens)


# ---------------------------------------------------------------------------
# Shared settings used across tests
# ---------------------------------------------------------------------------

SETTINGS = {
    "spacy": {
        "model": "en_core_web_sm",
        "filter_pos": ["DET", "PRON", "ADP", "AUX", "CCONJ", "SCONJ", "PART", "PUNCT"],
        "filter_ner": ["PERSON"],
    },
    "data": {
        "transcript_dir": "data/transcripts",
    },
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_nlp_cache():
    """Reset the module-level singleton before each test."""
    import src.analyzer as mod

    mod._nlp = None
    mod._nlp_model_name = None
    yield
    mod._nlp = None
    mod._nlp_model_name = None


@pytest.fixture()
def mock_spacy_load():
    """Patch spacy.load to return a callable mock model."""
    fake_nlp = MagicMock()
    with patch("src.analyzer.spacy") as mock_spacy:
        mock_spacy.load.return_value = fake_nlp
        yield mock_spacy, fake_nlp


# ===================================================================
# load_nlp tests
# ===================================================================


class TestLoadNlp:
    """Tests for the load_nlp function."""

    def test_loads_model_from_settings(self, mock_spacy_load):
        """load_nlp should call spacy.load with the configured model name."""
        from src.analyzer import load_nlp

        mock_spacy, fake_nlp = mock_spacy_load
        nlp = load_nlp(SETTINGS)

        mock_spacy.load.assert_called_once_with("en_core_web_sm")
        assert nlp is fake_nlp

    def test_singleton_caching(self, mock_spacy_load):
        """Calling load_nlp twice with same model should load only once."""
        from src.analyzer import load_nlp

        mock_spacy, fake_nlp = mock_spacy_load
        nlp1 = load_nlp(SETTINGS)
        nlp2 = load_nlp(SETTINGS)

        assert nlp1 is nlp2
        assert mock_spacy.load.call_count == 1

    def test_reloads_on_different_model(self, mock_spacy_load):
        """If model name changes, spacy.load should be called again."""
        from src.analyzer import load_nlp

        mock_spacy, _ = mock_spacy_load
        load_nlp(SETTINGS)

        other_settings = {
            "spacy": {"model": "en_core_web_md"},
        }
        load_nlp(other_settings)

        assert mock_spacy.load.call_count == 2

    def test_default_model_when_missing_key(self, mock_spacy_load):
        """When settings has empty spacy section, default to en_core_web_sm."""
        from src.analyzer import load_nlp

        mock_spacy, _ = mock_spacy_load
        load_nlp({"spacy": {}})
        mock_spacy.load.assert_called_once_with("en_core_web_sm")


# ===================================================================
# analyze_text tests
# ===================================================================


def _build_simple_doc(tokens_spec, ents_spec=None):
    """Build a _MockDoc from a compact specification.

    tokens_spec: list of (text, lemma, pos_)  — index is the token.i
    ents_spec:   list of (label_, [token_indices])
    """
    tokens = [
        _make_token(i, text, lemma, pos)
        for i, (text, lemma, pos) in enumerate(tokens_spec)
    ]

    ents = []
    if ents_spec:
        for label_, indices in ents_spec:
            ent_tokens = [tokens[j] for j in indices]
            ents.append(_MockEnt(label_, ent_tokens))

    # All tokens in one sentence
    sent = _MockSent(
        " ".join(t.text for t in tokens),
        tokens,
    )
    return _MockDoc(tokens, ents=ents, sents=[sent])


class TestAnalyzeText:
    """Tests for the analyze_text function."""

    def test_basic_word_extraction(self, mock_spacy_load):
        """Should extract content words and count frequencies."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        #  "The cat sat on the mat" — DET/ADP filtered
        doc = _build_simple_doc(
            [
                ("The", "the", "DET"),
                ("cat", "cat", "NOUN"),
                ("sat", "sit", "VERB"),
                ("on", "on", "ADP"),
                ("the", "the", "DET"),
                ("mat", "mat", "NOUN"),
            ]
        )
        fake_nlp.return_value = doc

        result = analyze_text("The cat sat on the mat", "ep1", SETTINGS)

        words = {v.word for v in result}
        assert "cat" in words
        assert "sit" in words  # lemma
        assert "mat" in words
        # filtered
        assert "the" not in words
        assert "on" not in words

    def test_function_word_filtering(self, mock_spacy_load):
        """DET, PRON, ADP, AUX, CCONJ, SCONJ, PART, PUNCT should be excluded."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        doc = _build_simple_doc(
            [
                ("I", "I", "PRON"),
                ("can", "can", "AUX"),
                ("run", "run", "VERB"),
                ("and", "and", "CCONJ"),
                ("jump", "jump", "VERB"),
                (".", ".", "PUNCT"),
            ]
        )
        fake_nlp.return_value = doc

        result = analyze_text("I can run and jump.", "ep1", SETTINGS)
        words = {v.word for v in result}

        assert "run" in words
        assert "jump" in words
        assert "i" not in words
        assert "can" not in words
        assert "and" not in words
        assert "." not in words

    def test_person_ner_filtering(self, mock_spacy_load):
        """Tokens belonging to PERSON entities must be excluded."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        doc = _build_simple_doc(
            [
                ("John", "John", "PROPN"),
                ("Smith", "Smith", "PROPN"),
                ("runs", "run", "VERB"),
                ("fast", "fast", "ADV"),
            ],
            ents_spec=[("PERSON", [0, 1])],
        )
        fake_nlp.return_value = doc

        result = analyze_text("John Smith runs fast", "ep1", SETTINGS)
        words = {v.word for v in result}

        assert "john" not in words
        assert "smith" not in words
        assert "run" in words
        assert "fast" in words

    def test_lemma_based_aggregation(self, mock_spacy_load):
        """Variants with the same lemma should be aggregated."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        doc = _build_simple_doc(
            [
                ("runs", "run", "VERB"),
                ("running", "run", "VERB"),
                ("ran", "run", "VERB"),
            ]
        )
        fake_nlp.return_value = doc

        result = analyze_text("runs running ran", "ep1", SETTINGS)

        assert len(result) == 1
        assert result[0].word == "run"
        assert result[0].frequency == 3

    def test_example_sentences_max_three(self, mock_spacy_load):
        """At most 3 example sentences should be collected per word."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        # 5 sentences, each containing "run"
        tokens = []
        sents = []
        idx = 0
        for s_idx in range(5):
            t = _make_token(idx, "run", "run", "VERB")
            tokens.append(t)
            sents.append(_MockSent(f"Sentence {s_idx}", [t]))
            idx += 1

        doc = _MockDoc(tokens, ents=[], sents=sents)
        fake_nlp.return_value = doc

        result = analyze_text("run run run run run", "ep1", SETTINGS)

        assert len(result) == 1
        assert result[0].frequency == 5
        assert len(result[0].example_sentences) == 3

    def test_empty_text(self, mock_spacy_load):
        """Empty input text should return an empty list."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        # Empty doc
        doc = _MockDoc([], ents=[], sents=[])
        fake_nlp.return_value = doc

        result = analyze_text("", "ep1", SETTINGS)
        assert result == []

    def test_sorted_by_frequency(self, mock_spacy_load):
        """Results should be sorted by frequency descending."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        doc = _build_simple_doc(
            [
                ("big", "big", "ADJ"),
                ("run", "run", "VERB"),
                ("run", "run", "VERB"),
                ("run", "run", "VERB"),
                ("big", "big", "ADJ"),
            ]
        )
        fake_nlp.return_value = doc

        result = analyze_text("big run run run big", "ep1", SETTINGS)

        assert result[0].word == "run"
        assert result[0].frequency == 3
        assert result[1].word == "big"
        assert result[1].frequency == 2

    def test_episodes_list(self, mock_spacy_load):
        """Each vocabulary item should have the episode_id in its episodes list."""
        from src.analyzer import analyze_text

        _, fake_nlp = mock_spacy_load

        doc = _build_simple_doc([("hello", "hello", "INTJ")])
        fake_nlp.return_value = doc

        result = analyze_text("hello", "ep42", SETTINGS)
        assert result[0].episodes == ["ep42"]


# ===================================================================
# analyze_episode tests
# ===================================================================


class TestAnalyzeEpisode:
    """Tests for the analyze_episode function."""

    def test_normal_episode(self, tmp_path, mock_spacy_load):
        """Should load transcript JSON and return vocab list."""
        from src.analyzer import analyze_episode

        _, fake_nlp = mock_spacy_load

        # Prepare transcript file
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)
        transcript = {"full_text": "The cat sat", "sentences": []}
        (transcript_dir / "ep1_official.json").write_text(
            json.dumps(transcript), encoding="utf-8"
        )

        doc = _build_simple_doc(
            [
                ("The", "the", "DET"),
                ("cat", "cat", "NOUN"),
                ("sat", "sit", "VERB"),
            ]
        )
        fake_nlp.return_value = doc

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_episode("ep1", settings)

        assert len(result) > 0
        words = {v.word for v in result}
        assert "cat" in words

    def test_file_not_found(self, tmp_path, mock_spacy_load):
        """Should raise FileNotFoundError when transcript is missing."""
        from src.analyzer import analyze_episode

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            with pytest.raises(FileNotFoundError):
                analyze_episode("nonexistent", settings)

    def test_fallback_to_sentences(self, tmp_path, mock_spacy_load):
        """When full_text is empty, should join sentences as fallback."""
        from src.analyzer import analyze_episode

        _, fake_nlp = mock_spacy_load

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)
        transcript = {
            "full_text": "",
            "sentences": ["Hello world", "Good morning"],
        }
        (transcript_dir / "ep2_official.json").write_text(
            json.dumps(transcript), encoding="utf-8"
        )

        doc = _build_simple_doc(
            [
                ("Hello", "hello", "INTJ"),
                ("world", "world", "NOUN"),
                ("Good", "good", "ADJ"),
                ("morning", "morning", "NOUN"),
            ]
        )
        fake_nlp.return_value = doc

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_episode("ep2", settings)

        assert len(result) > 0

    def test_empty_transcript(self, tmp_path, mock_spacy_load):
        """Episode with empty full_text and no sentences returns empty list."""
        from src.analyzer import analyze_episode

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)
        transcript = {"full_text": "", "sentences": []}
        (transcript_dir / "ep3_official.json").write_text(
            json.dumps(transcript), encoding="utf-8"
        )

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_episode("ep3", settings)

        assert result == []


# ===================================================================
# analyze_all tests
# ===================================================================


class TestAnalyzeAll:
    """Tests for the analyze_all batch function."""

    def test_merge_across_episodes(self, tmp_path, mock_spacy_load):
        """Frequencies and episodes should merge for the same (word, pos)."""
        from src.analyzer import analyze_all

        _, fake_nlp = mock_spacy_load

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        for ep_id in ("ep1", "ep2"):
            data = {"full_text": "run fast", "sentences": []}
            (transcript_dir / f"{ep_id}_official.json").write_text(
                json.dumps(data), encoding="utf-8"
            )

        doc = _build_simple_doc(
            [
                ("run", "run", "VERB"),
                ("fast", "fast", "ADV"),
            ]
        )
        fake_nlp.return_value = doc

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_all(["ep1", "ep2"], settings)

        run_vocab = next(v for v in result if v.word == "run")
        assert run_vocab.frequency == 2
        assert set(run_vocab.episodes) == {"ep1", "ep2"}

    def test_partial_failure(self, tmp_path, mock_spacy_load):
        """If one episode is missing, the others should still be processed."""
        from src.analyzer import analyze_all

        _, fake_nlp = mock_spacy_load

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        data = {"full_text": "hello", "sentences": []}
        (transcript_dir / "ep_ok_official.json").write_text(
            json.dumps(data), encoding="utf-8"
        )
        # ep_missing does NOT have a file

        doc = _build_simple_doc([("hello", "hello", "INTJ")])
        fake_nlp.return_value = doc

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_all(["ep_ok", "ep_missing"], settings)

        assert len(result) == 1
        assert result[0].word == "hello"

    def test_empty_episode_list(self, mock_spacy_load):
        """Calling with no episodes should return empty list."""
        from src.analyzer import analyze_all

        result = analyze_all([], SETTINGS)
        assert result == []

    def test_example_sentences_merged(self, tmp_path, mock_spacy_load):
        """Example sentences from different episodes should be combined."""
        from src.analyzer import analyze_all

        _, fake_nlp = mock_spacy_load

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        for ep_id in ("epA", "epB"):
            data = {"full_text": "test word", "sentences": []}
            (transcript_dir / f"{ep_id}_official.json").write_text(
                json.dumps(data), encoding="utf-8"
            )

        # We need fake_nlp to return docs with episode-specific sentence text.
        # Since analyze_text is called per episode, we can return the same doc
        # but example sentences will differ because episode_id differs.
        doc = _build_simple_doc(
            [
                ("test", "test", "NOUN"),
                ("word", "word", "NOUN"),
            ]
        )
        fake_nlp.return_value = doc

        settings = {
            **SETTINGS,
            "data": {"transcript_dir": "data/transcripts"},
        }

        with patch("src.analyzer._PROJECT_ROOT", tmp_path):
            result = analyze_all(["epA", "epB"], settings)

        test_vocab = next(v for v in result if v.word == "test")
        # Same sentence text but different episode_ids — both should appear
        ep_ids_in_examples = {ex.episode_id for ex in test_vocab.example_sentences}
        assert "epA" in ep_ids_in_examples
        assert "epB" in ep_ids_in_examples
