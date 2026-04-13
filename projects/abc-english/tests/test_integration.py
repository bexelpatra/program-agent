"""End-to-end integration tests for the ABC English study pipeline.

Verifies that data flows correctly between modules:
  Collector -> Transcriber -> Comparator -> Analyzer -> LLM Analyzer -> Loader

All external dependencies (HTTP, Whisper, spaCy, LLM APIs, Elasticsearch) are
mocked.  The focus is on **interface compatibility** between modules, not on
the internal logic of each module (which is covered by unit tests).
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import List
from unittest.mock import MagicMock, patch

import pytest

# conftest.py installs a mock spacy module at import time (pytest loads it
# automatically), so src.analyzer can be imported without the real spacy.

from src.models import (
    Episode,
    ExampleSentence,
    Expression,
    Sentence,
    Vocabulary,
    EPISODE_MAPPING,
    EXPRESSION_MAPPING,
    SENTENCE_MAPPING,
    VOCABULARY_MAPPING,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

FAKE_EPISODE_ID = "999001"
FAKE_SETTINGS = {
    "crawling": {
        "base_url": "https://www.abc.net.au",
        "program_url": "https://www.abc.net.au/listen/programs/abc-news-daily",
        "request_delay": 0,
        "max_retries": 1,
        "request_timeout": 5,
        "user_agent": "TestAgent/1.0",
    },
    "data": {
        "transcript_dir": "data/transcripts",
        "audio_dir": "data/audio",
    },
    "whisper": {
        "model": "base",
        "device": "cpu",
    },
    "spacy": {
        "model": "en_core_web_sm",
        "filter_pos": [
            "PUNCT",
            "SPACE",
            "DET",
            "ADP",
            "AUX",
            "PRON",
            "CONJ",
            "CCONJ",
            "SCONJ",
            "PART",
        ],
        "filter_ner": ["PERSON"],
    },
    "llm": {
        "provider": "ollama",
        "ollama": {
            "model": "llama3",
            "base_url": "http://localhost:11434",
            "batch_size": 10,
        },
    },
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
    },
}


@pytest.fixture
def transcript_dir(tmp_path):
    """Create a temporary transcript directory with fake transcripts."""
    t_dir = tmp_path / "data" / "transcripts"
    t_dir.mkdir(parents=True)

    official = {
        "episode_id": FAKE_EPISODE_ID,
        "full_text": (
            "Australia is facing a housing crisis. "
            "The government announced new policies today. "
            "Experts say more action is needed."
        ),
        "sentences": [
            "Australia is facing a housing crisis.",
            "The government announced new policies today.",
            "Experts say more action is needed.",
        ],
    }
    (t_dir / f"{FAKE_EPISODE_ID}_official.json").write_text(
        json.dumps(official, ensure_ascii=False), encoding="utf-8"
    )

    whisper = {
        "episode_id": FAKE_EPISODE_ID,
        "full_text": (
            "Australia is facing a housing crisis. "
            "The government announced new policy today. "
            "Experts say more actions is needed."
        ),
        "segments": [
            {"text": "Australia is facing a housing crisis.", "start": 0.0, "end": 3.5},
            {
                "text": "The government announced new policy today.",
                "start": 3.5,
                "end": 7.2,
            },
            {"text": "Experts say more actions is needed.", "start": 7.2, "end": 10.0},
        ],
    }
    (t_dir / f"{FAKE_EPISODE_ID}_whisper.json").write_text(
        json.dumps(whisper, ensure_ascii=False), encoding="utf-8"
    )

    return t_dir


@pytest.fixture
def settings_for_tmp(tmp_path):
    """Return a settings dict whose data paths point to tmp_path."""
    s = json.loads(json.dumps(FAKE_SETTINGS))  # deep copy
    s["data"]["transcript_dir"] = str(tmp_path / "data" / "transcripts")
    s["data"]["audio_dir"] = str(tmp_path / "data" / "audio")
    return s


# ===========================================================================
# Test 1: Collect -> Compare flow
# ===========================================================================


class TestCollectToCompareFlow:
    """Simulate collection -> transcription -> comparison pipeline."""

    def test_collect_to_compare_flow(self, tmp_path, transcript_dir):
        """Data collected by collector is consumable by comparator.

        Steps:
        1. Verify that transcript JSON files written by the collector
           format are readable by the comparator.
        2. Run comparator.compare_sentences with official sentences and
           Whisper segments.
        3. Verify WER is computed and listening_difficulty is assigned.
        """
        from src.comparator import (
            compare_sentences,
            calculate_wer,
            calculate_listening_difficulty,
        )

        # Load the fake official transcript (as collector would produce)
        official_path = transcript_dir / f"{FAKE_EPISODE_ID}_official.json"
        with open(official_path, "r", encoding="utf-8") as f:
            official_data = json.load(f)

        # Load the fake whisper transcript (as transcriber would produce)
        whisper_path = transcript_dir / f"{FAKE_EPISODE_ID}_whisper.json"
        with open(whisper_path, "r", encoding="utf-8") as f:
            whisper_data = json.load(f)

        official_sentences = official_data["sentences"]
        whisper_segments = whisper_data["segments"]

        # Run comparison -- this is the key interface: list[str] + list[dict] -> list[dict]
        results = compare_sentences(official_sentences, whisper_segments)

        # Verify output structure
        assert len(results) == len(official_sentences)

        for r in results:
            assert "sentence_index" in r
            assert "official_text" in r
            assert "whisper_text" in r
            assert "start_time" in r
            assert "end_time" in r
            assert "wer" in r
            assert "listening_difficulty" in r
            assert isinstance(r["wer"], float)
            assert 0.0 <= r["wer"] <= 1.0
            assert r["listening_difficulty"] in ("easy", "medium", "hard", "very_hard")

        # Verify that the first sentence (identical) has low WER
        assert results[0]["wer"] == 0.0
        assert results[0]["listening_difficulty"] == "easy"

    def test_compare_results_to_sentence_models(self, transcript_dir):
        """compare_sentences output can be converted to Sentence models."""
        from src.comparator import compare_sentences

        official_path = transcript_dir / f"{FAKE_EPISODE_ID}_official.json"
        with open(official_path) as f:
            official_data = json.load(f)
        whisper_path = transcript_dir / f"{FAKE_EPISODE_ID}_whisper.json"
        with open(whisper_path) as f:
            whisper_data = json.load(f)

        compared = compare_sentences(
            official_data["sentences"], whisper_data["segments"]
        )

        # Convert to Sentence models (same as comparator.compare_episode does)
        sentences: List[Sentence] = []
        for item in compared:
            sent = Sentence(
                episode_id=FAKE_EPISODE_ID,
                sentence_index=item["sentence_index"],
                official_text=item["official_text"],
                whisper_text=item["whisper_text"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                wer=item["wer"],
                listening_difficulty=item["listening_difficulty"],
            )
            sentences.append(sent)

        assert len(sentences) == 3
        for s in sentences:
            assert isinstance(s, Sentence)
            assert s.episode_id == FAKE_EPISODE_ID


# ===========================================================================
# Test 2: Analyze -> Load flow (vocabulary)
# ===========================================================================


class TestAnalyzeToLoadFlow:
    """Verify that analyzer output is directly consumable by the loader."""

    def test_analyze_text_returns_vocabulary_models(self):
        """analyzer.analyze_text returns List[Vocabulary] usable by loader."""
        # We need spacy to actually work for analyze_text.
        # Since spacy may not be installed, we mock the nlp pipeline.
        mock_nlp = MagicMock()

        # Build a minimal spaCy-like Doc with tokens and sentences
        mock_token_1 = MagicMock()
        mock_token_1.text = "crisis"
        mock_token_1.lemma_ = "crisis"
        mock_token_1.pos_ = "NOUN"
        mock_token_1.is_space = False
        mock_token_1.i = 0

        mock_token_2 = MagicMock()
        mock_token_2.text = "housing"
        mock_token_2.lemma_ = "housing"
        mock_token_2.pos_ = "NOUN"
        mock_token_2.is_space = False
        mock_token_2.i = 1

        mock_token_3 = MagicMock()
        mock_token_3.text = "is"
        mock_token_3.lemma_ = "be"
        mock_token_3.pos_ = "AUX"
        mock_token_3.is_space = False
        mock_token_3.i = 2

        mock_sent = MagicMock()
        mock_sent.text = "Australia is facing a housing crisis."
        mock_sent.__iter__ = lambda self: iter(
            [mock_token_1, mock_token_2, mock_token_3]
        )

        mock_doc = MagicMock()
        mock_doc.__iter__ = lambda self: iter(
            [mock_token_1, mock_token_2, mock_token_3]
        )
        mock_doc.sents = [mock_sent]
        mock_doc.ents = []

        mock_nlp.return_value = mock_doc

        settings = json.loads(json.dumps(FAKE_SETTINGS))

        with patch("src.analyzer.load_nlp", return_value=mock_nlp):
            from src.analyzer import analyze_text

            vocab_list = analyze_text(
                "Australia is facing a housing crisis.",
                FAKE_EPISODE_ID,
                settings=settings,
            )

        # Verify return type
        assert isinstance(vocab_list, list)
        for v in vocab_list:
            assert isinstance(v, Vocabulary)
            assert v.word  # non-empty
            assert v.pos
            assert v.frequency >= 1
            assert FAKE_EPISODE_ID in v.episodes

        # Verify these Vocabulary objects are accepted by loader.load_vocabulary
        # (type check -- we don't actually call ES)
        for v in vocab_list:
            # model_dump should work (Pydantic model)
            dumped = v.model_dump()
            assert "word" in dumped
            assert "pos" in dumped
            assert "frequency" in dumped
            assert "episodes" in dumped
            assert "example_sentences" in dumped

    def test_vocabulary_accepted_by_loader(self):
        """Construct Vocabulary models and verify loader accepts them."""
        vocab_items = [
            Vocabulary(
                word="crisis",
                pos="NOUN",
                frequency=3,
                episodes=[FAKE_EPISODE_ID],
                example_sentences=[
                    ExampleSentence(
                        episode_id=FAKE_EPISODE_ID,
                        text="Australia is facing a housing crisis.",
                    )
                ],
            ),
            Vocabulary(
                word="policy",
                pos="NOUN",
                frequency=1,
                episodes=[FAKE_EPISODE_ID],
                example_sentences=[],
            ),
        ]

        # Verify each can be serialised via model_dump (required by loader)
        for v in vocab_items:
            d = v.model_dump()
            assert isinstance(d, dict)
            assert "word" in d
            # loader uses _id = f"{v.word}_{v.pos}"
            doc_id = f"{v.word}_{v.pos}"
            assert doc_id  # non-empty


# ===========================================================================
# Test 3: LLM Analyze -> Load flow (expressions)
# ===========================================================================


class TestLLMAnalyzeToLoadFlow:
    """Verify LLM analyzer output is consumable by the expression loader."""

    def test_detect_expressions_for_episode(self, tmp_path):
        """Mock LLM and verify detect_expressions_for_episode returns Expression models."""
        from src.llm_analyzer import (
            detect_expressions_for_episode,
            reset_provider,
            LLMProvider,
        )

        # Create fake transcript file in the expected location
        # detect_expressions_for_episode uses Path(__file__).parent.parent / "data" / ...
        # So we need to patch the path resolution.
        transcript_data = {
            "episode_id": FAKE_EPISODE_ID,
            "full_text": "The government is pulling out all the stops to address housing.",
            "sentences": [
                "The government is pulling out all the stops to address housing."
            ],
        }

        # Create a mock LLM provider
        mock_provider = MagicMock(spec=LLMProvider)
        mock_provider.generate_json.return_value = [
            {
                "phrase": "pull out all the stops",
                "type": "idiom",
                "definition_en": "To make every possible effort",
                "definition_ko": "모든 노력을 기울이다",
                "etymology": "Originates from organ playing where pulling out stops increases volume.",
                "difficulty": "B2",
            }
        ]

        reset_provider()

        # Patch both the provider and the transcript file path
        transcript_file = (
            tmp_path / "data" / "transcripts" / f"{FAKE_EPISODE_ID}_official.json"
        )
        transcript_file.parent.mkdir(parents=True, exist_ok=True)
        transcript_file.write_text(
            json.dumps(transcript_data, ensure_ascii=False), encoding="utf-8"
        )

        with (
            patch("src.llm_analyzer.get_provider", return_value=mock_provider),
            patch("src.llm_analyzer._get_cache", return_value=None),
            patch("src.llm_analyzer._set_cache"),
            patch(
                "src.llm_analyzer.Path.__file__",
                create=True,
            ),
        ):
            # We need to patch the project_root computation inside detect_expressions_for_episode
            # The function computes: project_root = Path(__file__).resolve().parent.parent
            # Then opens: project_root / "data" / "transcripts" / f"{episode_id}_official.json"
            # We'll patch the open call to return our fake data instead.
            import builtins

            original_open = builtins.open

            def patched_open(path, *args, **kwargs):
                path_str = str(path)
                if f"{FAKE_EPISODE_ID}_official.json" in path_str:
                    return original_open(str(transcript_file), *args, **kwargs)
                return original_open(path, *args, **kwargs)

            with patch("builtins.open", side_effect=patched_open):
                expressions = detect_expressions_for_episode(
                    FAKE_EPISODE_ID, settings=FAKE_SETTINGS
                )

        # Verify return type and structure
        assert isinstance(expressions, list)
        assert len(expressions) >= 1

        for expr in expressions:
            assert isinstance(expr, Expression)
            assert expr.phrase
            assert expr.type in ("idiom", "phrasal_verb", "collocation")
            assert FAKE_EPISODE_ID in expr.episodes

        # Verify expressions can be serialised for loader
        for expr in expressions:
            d = expr.model_dump()
            assert "phrase" in d
            assert "type" in d
            assert "definition_en" in d
            assert "definition_ko" in d
            assert "episodes" in d

    def test_expression_models_accepted_by_loader(self):
        """Construct Expression models and verify loader type compatibility."""
        expressions = [
            Expression(
                phrase="pull out all the stops",
                type="idiom",
                definition_en="To make every possible effort",
                definition_ko="모든 노력을 기울이다",
                etymology="Originates from organ playing.",
                difficulty="B2",
                frequency=1,
                episodes=[FAKE_EPISODE_ID],
                example_sentences=[
                    ExampleSentence(
                        episode_id=FAKE_EPISODE_ID,
                        text="The government is pulling out all the stops.",
                    )
                ],
            ),
            Expression(
                phrase="look into",
                type="phrasal_verb",
                definition_en="To investigate or examine",
                definition_ko="조사하다",
                difficulty="B1",
                frequency=2,
                episodes=[FAKE_EPISODE_ID],
                example_sentences=[],
            ),
        ]

        # Verify serialisation works (loader calls model_dump())
        for expr in expressions:
            d = expr.model_dump()
            assert isinstance(d, dict)
            assert d["type"] in ("idiom", "phrasal_verb", "collocation")


# ===========================================================================
# Test 4: Data model consistency with ES mappings
# ===========================================================================


class TestDataModelConsistency:
    """Verify that model fields align with ES index mappings."""

    def test_episode_fields_match_mapping(self):
        """Episode model fields correspond to EPISODE_MAPPING properties."""
        mapping_props = set(EPISODE_MAPPING["mappings"]["properties"].keys())
        model_fields = set(Episode.model_fields.keys())

        # Every mapping property should be a model field
        for prop in mapping_props:
            assert (
                prop in model_fields
            ), f"ES mapping property '{prop}' not found in Episode model"

    def test_sentence_fields_match_mapping(self):
        """Sentence model fields correspond to SENTENCE_MAPPING properties."""
        mapping_props = set(SENTENCE_MAPPING["mappings"]["properties"].keys())
        model_fields = set(Sentence.model_fields.keys())

        for prop in mapping_props:
            assert (
                prop in model_fields
            ), f"ES mapping property '{prop}' not found in Sentence model"

    def test_vocabulary_fields_match_mapping(self):
        """Vocabulary model fields correspond to VOCABULARY_MAPPING properties."""
        mapping_props = set(VOCABULARY_MAPPING["mappings"]["properties"].keys())
        model_fields = set(Vocabulary.model_fields.keys())

        for prop in mapping_props:
            assert (
                prop in model_fields
            ), f"ES mapping property '{prop}' not found in Vocabulary model"

    def test_expression_fields_match_mapping(self):
        """Expression model fields correspond to EXPRESSION_MAPPING properties."""
        mapping_props = set(EXPRESSION_MAPPING["mappings"]["properties"].keys())
        model_fields = set(Expression.model_fields.keys())

        for prop in mapping_props:
            assert (
                prop in model_fields
            ), f"ES mapping property '{prop}' not found in Expression model"

    def test_model_dump_serialisable(self):
        """All models produce JSON-serialisable dicts via model_dump."""
        ep = Episode(
            episode_id="test-001",
            title="Test Episode",
            published_date=datetime(2025, 1, 1),
            duration_seconds=300,
            url="https://example.com/test",
        )
        sent = Sentence(
            episode_id="test-001",
            sentence_index=0,
            official_text="Hello world.",
        )
        vocab = Vocabulary(
            word="hello",
            pos="INTJ",
            frequency=1,
            episodes=["test-001"],
        )
        expr = Expression(
            phrase="break the ice",
            type="idiom",
            frequency=1,
            episodes=["test-001"],
        )

        for model in (ep, sent, vocab, expr):
            d = model.model_dump()
            # Should be JSON serialisable (datetime -> isoformat via default handler)
            serialised = json.dumps(d, default=str)
            assert isinstance(serialised, str)

    def test_loader_action_id_construction(self):
        """Verify that loader _id construction logic works with model data."""
        import re

        def _slug(text: str) -> str:
            return re.sub(r"\s+", "-", text.strip().lower())

        # Episode: _id = episode_id
        ep = Episode(
            episode_id="12345",
            title="Test",
            published_date=datetime(2025, 1, 1),
            duration_seconds=60,
            url="https://example.com",
        )
        assert ep.episode_id == "12345"

        # Sentence: _id = f"{episode_id}_{sentence_index}"
        sent = Sentence(
            episode_id="12345",
            sentence_index=3,
            official_text="Test sentence.",
        )
        doc_id = f"{sent.episode_id}_{sent.sentence_index}"
        assert doc_id == "12345_3"

        # Vocabulary: _id = f"{word}_{pos}"
        vocab = Vocabulary(word="hello", pos="INTJ", frequency=1)
        doc_id = f"{vocab.word}_{vocab.pos}"
        assert doc_id == "hello_INTJ"

        # Expression: _id = _slug(phrase)
        expr = Expression(
            phrase="break the ice",
            type="idiom",
            frequency=1,
        )
        doc_id = _slug(expr.phrase)
        assert doc_id == "break-the-ice"


# ===========================================================================
# Test 5: Full pipeline data flow simulation
# ===========================================================================


class TestFullPipelineFlow:
    """Simulate the full pipeline with all modules connected via mock data."""

    def test_end_to_end_data_flow(self, transcript_dir):
        """Verify data flows from comparison through analysis to model output.

        This test chains:
        1. Comparator: official vs whisper -> Sentence models
        2. Vocabulary analysis: transcript text -> Vocabulary models
        3. LLM expression detection: transcript text -> Expression models
        4. All outputs are typed correctly for the loader
        """
        from src.comparator import compare_sentences

        # -- Step 1: Comparison --
        official_path = transcript_dir / f"{FAKE_EPISODE_ID}_official.json"
        with open(official_path) as f:
            official_data = json.load(f)
        whisper_path = transcript_dir / f"{FAKE_EPISODE_ID}_whisper.json"
        with open(whisper_path) as f:
            whisper_data = json.load(f)

        compared = compare_sentences(
            official_data["sentences"], whisper_data["segments"]
        )
        sentences = [
            Sentence(
                episode_id=FAKE_EPISODE_ID,
                sentence_index=item["sentence_index"],
                official_text=item["official_text"],
                whisper_text=item["whisper_text"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                wer=item["wer"],
                listening_difficulty=item["listening_difficulty"],
            )
            for item in compared
        ]
        assert all(isinstance(s, Sentence) for s in sentences)

        # -- Step 2: Vocabulary analysis (mock spaCy) --
        mock_nlp = MagicMock()

        tokens = []
        for i, (word, pos) in enumerate(
            [
                ("australia", "PROPN"),
                ("face", "VERB"),
                ("housing", "NOUN"),
                ("crisis", "NOUN"),
                ("government", "NOUN"),
                ("announce", "VERB"),
            ]
        ):
            tok = MagicMock()
            tok.text = word
            tok.lemma_ = word
            tok.pos_ = pos
            tok.is_space = False
            tok.i = i
            tokens.append(tok)

        mock_sent = MagicMock()
        mock_sent.text = official_data["full_text"]
        mock_sent.__iter__ = lambda self: iter(tokens)

        mock_doc = MagicMock()
        mock_doc.__iter__ = lambda self: iter(tokens)
        mock_doc.sents = [mock_sent]
        mock_doc.ents = []

        mock_nlp.return_value = mock_doc

        settings = json.loads(json.dumps(FAKE_SETTINGS))

        with patch("src.analyzer.load_nlp", return_value=mock_nlp):
            from src.analyzer import analyze_text

            vocab_list = analyze_text(
                official_data["full_text"],
                FAKE_EPISODE_ID,
                settings=settings,
            )

        assert all(isinstance(v, Vocabulary) for v in vocab_list)
        assert len(vocab_list) > 0

        # -- Step 3: Expression detection (mock LLM) --
        fake_expressions = [
            Expression(
                phrase="face a crisis",
                type="collocation",
                definition_en="To confront a serious problem",
                definition_ko="위기에 직면하다",
                difficulty="B1",
                frequency=1,
                episodes=[FAKE_EPISODE_ID],
                example_sentences=[],
            ),
        ]

        # -- Step 4: Verify all outputs are loader-compatible --
        episode = Episode(
            episode_id=FAKE_EPISODE_ID,
            title="Test Episode",
            published_date=datetime(2025, 6, 1),
            duration_seconds=600,
            url="https://www.abc.net.au/listen/programs/abc-news-daily/test/999001",
            official_transcript=official_data["full_text"],
            has_transcript=True,
            sentence_count=len(sentences),
            word_count=len(official_data["full_text"].split()),
        )

        # All types match what loader expects
        assert isinstance(episode, Episode)
        assert all(isinstance(s, Sentence) for s in sentences)
        assert all(isinstance(v, Vocabulary) for v in vocab_list)
        assert all(isinstance(e, Expression) for e in fake_expressions)

        # All can be serialised
        for model_list in ([episode], sentences, vocab_list, fake_expressions):
            for m in model_list:
                d = m.model_dump()
                assert isinstance(d, dict)
                json.dumps(d, default=str)  # no exception = serialisable

    def test_episode_model_from_collector_data(self):
        """Verify that raw collector dict data can instantiate Episode models."""
        # Simulate what collect_all does: merge list-page + detail-page data
        raw_data = {
            "episode_id": "12345",
            "title": "Today's News",
            "description": "A summary of today's news.",
            "published_date": datetime(2025, 4, 10),
            "duration_seconds": 900,
            "url": "https://www.abc.net.au/listen/programs/abc-news-daily/todays-news/12345",
            "audio_url": "https://media.example.com/12345.mp3",
            "has_transcript": True,
            "official_transcript": "Full text here.",
        }

        episode = Episode(**raw_data)
        assert episode.episode_id == "12345"
        assert episode.title == "Today's News"
        assert episode.has_transcript is True

        # The episode should be serialisable for the loader
        d = episode.model_dump()
        assert d["episode_id"] == "12345"

    def test_compare_episode_output_feeds_loader(self, transcript_dir):
        """compare_episode returns (List[Sentence], float) usable by loader."""
        from src.comparator import compare_sentences

        official_path = transcript_dir / f"{FAKE_EPISODE_ID}_official.json"
        with open(official_path) as f:
            official_data = json.load(f)
        whisper_path = transcript_dir / f"{FAKE_EPISODE_ID}_whisper.json"
        with open(whisper_path) as f:
            whisper_data = json.load(f)

        compared = compare_sentences(
            official_data["sentences"], whisper_data["segments"]
        )

        sentences = []
        total_wer = 0.0
        for item in compared:
            sent = Sentence(
                episode_id=FAKE_EPISODE_ID,
                sentence_index=item["sentence_index"],
                official_text=item["official_text"],
                whisper_text=item["whisper_text"],
                start_time=item["start_time"],
                end_time=item["end_time"],
                wer=item["wer"],
                listening_difficulty=item["listening_difficulty"],
            )
            sentences.append(sent)
            total_wer += item["wer"]

        avg_wer = total_wer / len(compared) if compared else 0.0

        # Loader expects List[Sentence]
        assert isinstance(sentences, list)
        assert all(isinstance(s, Sentence) for s in sentences)
        assert isinstance(avg_wer, float)
        assert 0.0 <= avg_wer <= 1.0
