"""Unit tests for src/comparator.py.

File I/O uses pytest's tmp_path fixture.  The module-level _PROJECT_ROOT
is patched to redirect file lookups to temporary directories.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import src.comparator as comparator_module

from src.comparator import (
    calculate_listening_difficulty,
    calculate_wer,
    compare_all,
    compare_episode,
    compare_sentences,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

SETTINGS = {
    "data": {
        "transcript_dir": "data/transcripts",
    },
}


# ---------------------------------------------------------------------------
# calculate_wer
# ---------------------------------------------------------------------------


class TestCalculateWer:
    def test_identical_text(self):
        """Identical strings should yield WER = 0.0."""
        assert calculate_wer("hello world", "hello world") == 0.0

    def test_completely_different(self):
        """Completely different words should yield WER = 1.0."""
        wer = calculate_wer("hello world", "foo bar")
        assert wer == 1.0

    def test_both_empty(self):
        """Both empty strings should yield WER = 0.0."""
        assert calculate_wer("", "") == 0.0

    def test_reference_empty_hypothesis_not(self):
        """Empty reference with non-empty hypothesis should yield WER = 1.0."""
        assert calculate_wer("", "some words") == 1.0

    def test_hypothesis_empty_reference_not(self):
        """Non-empty reference with empty hypothesis: all words are deletions."""
        wer = calculate_wer("hello world", "")
        # 2 deletions / 2 reference words = 1.0
        assert wer == 1.0

    def test_punctuation_ignored(self):
        """Punctuation differences should not affect WER."""
        wer = calculate_wer(
            "Hello, world! How are you?",
            "Hello world How are you",
        )
        assert wer == 0.0

    def test_case_insensitive(self):
        """WER comparison should be case-insensitive."""
        assert calculate_wer("Hello World", "hello world") == 0.0

    def test_partial_match(self):
        """One substitution in two words gives WER = 0.5."""
        wer = calculate_wer("hello world", "hello earth")
        assert wer == pytest.approx(0.5)

    def test_insertion(self):
        """Extra words in hypothesis count as insertions."""
        wer = calculate_wer("the cat", "the big cat")
        # 1 insertion / 2 reference words = 0.5
        assert wer == pytest.approx(0.5)

    def test_deletion(self):
        """Missing words in hypothesis count as deletions."""
        wer = calculate_wer("the big cat", "the cat")
        # 1 deletion / 3 reference words = 0.333...
        assert wer == pytest.approx(1 / 3)


# ---------------------------------------------------------------------------
# calculate_listening_difficulty
# ---------------------------------------------------------------------------


class TestCalculateListeningDifficulty:
    def test_easy(self):
        assert calculate_listening_difficulty(0.0) == "easy"
        assert calculate_listening_difficulty(0.05) == "easy"

    def test_medium(self):
        assert calculate_listening_difficulty(0.06) == "medium"
        assert calculate_listening_difficulty(0.15) == "medium"

    def test_hard(self):
        assert calculate_listening_difficulty(0.16) == "hard"
        assert calculate_listening_difficulty(0.30) == "hard"

    def test_very_hard(self):
        assert calculate_listening_difficulty(0.31) == "very_hard"
        assert calculate_listening_difficulty(1.0) == "very_hard"

    def test_boundary_easy_medium(self):
        """0.05 is easy, 0.050001 is medium."""
        assert calculate_listening_difficulty(0.05) == "easy"
        assert calculate_listening_difficulty(0.050001) == "medium"

    def test_boundary_medium_hard(self):
        assert calculate_listening_difficulty(0.15) == "medium"
        assert calculate_listening_difficulty(0.150001) == "hard"

    def test_boundary_hard_very_hard(self):
        assert calculate_listening_difficulty(0.30) == "hard"
        assert calculate_listening_difficulty(0.300001) == "very_hard"


# ---------------------------------------------------------------------------
# compare_sentences
# ---------------------------------------------------------------------------


class TestCompareSentences:
    def test_normal_matching(self):
        official = ["Hello world.", "How are you?"]
        segments = [
            {"text": "Hello world.", "start": 0.0, "end": 1.5},
            {"text": "How are you?", "start": 1.5, "end": 3.0},
        ]

        results = compare_sentences(official, segments)

        assert len(results) == 2
        assert results[0]["sentence_index"] == 0
        assert results[0]["official_text"] == "Hello world."
        assert results[0]["whisper_text"] == "Hello world."
        assert results[0]["wer"] == 0.0
        assert results[0]["listening_difficulty"] == "easy"

    def test_segments_exhausted(self):
        """When whisper segments run out, remaining sentences get WER=1.0."""
        official = ["First sentence.", "Second sentence.", "Third sentence."]
        segments = [
            {"text": "First sentence.", "start": 0.0, "end": 1.0},
        ]

        results = compare_sentences(official, segments)

        assert len(results) == 3
        # First sentence matched
        assert results[0]["whisper_text"] == "First sentence."
        # Remaining sentences have no whisper match
        assert results[1]["whisper_text"] == ""
        assert results[1]["wer"] == 1.0
        assert results[2]["whisper_text"] == ""
        assert results[2]["wer"] == 1.0

    def test_empty_official(self):
        """Empty official sentences list should return empty results."""
        results = compare_sentences([], [{"text": "Something", "start": 0, "end": 1}])
        assert results == []

    def test_empty_segments(self):
        """All official sentences without segments get WER=1.0."""
        results = compare_sentences(["Hello.", "World."], [])
        assert len(results) == 2
        assert all(r["wer"] == 1.0 for r in results)

    def test_both_empty(self):
        results = compare_sentences([], [])
        assert results == []

    def test_last_sentence_consumes_all_remaining(self):
        """The last official sentence should consume all remaining segments."""
        official = ["Short.", "Long final sentence."]
        segments = [
            {"text": "Short.", "start": 0.0, "end": 0.5},
            {"text": "Long", "start": 0.5, "end": 1.0},
            {"text": "final", "start": 1.0, "end": 1.5},
            {"text": "sentence.", "start": 1.5, "end": 2.0},
        ]

        results = compare_sentences(official, segments)

        assert len(results) == 2
        # Last sentence accumulates all remaining segments
        assert "Long" in results[1]["whisper_text"]
        assert "sentence." in results[1]["whisper_text"]

    def test_start_end_times_from_segments(self):
        official = ["Test sentence."]
        segments = [
            {"text": "Test", "start": 5.0, "end": 5.5},
            {"text": "sentence.", "start": 5.5, "end": 6.0},
        ]

        results = compare_sentences(official, segments)

        assert results[0]["start_time"] == 5.0
        assert results[0]["end_time"] == 6.0


# ---------------------------------------------------------------------------
# compare_episode
# ---------------------------------------------------------------------------


class TestCompareEpisode:
    def test_normal_comparison(self, tmp_path):
        """Load official + whisper JSON, compare, return Sentence models."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        official_data = {
            "episode_id": "ep100",
            "sentences": [
                "The government announced new policies.",
                "Citizens reacted positively.",
            ],
        }
        whisper_data = {
            "episode_id": "ep100",
            "segments": [
                {
                    "text": "The government announced new policies.",
                    "start": 0.0,
                    "end": 3.0,
                },
                {"text": "Citizens reacted positively.", "start": 3.0, "end": 5.0},
            ],
        }

        with open(transcript_dir / "ep100_official.json", "w") as f:
            json.dump(official_data, f)
        with open(transcript_dir / "ep100_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            sentences, avg_wer = compare_episode("ep100", settings=SETTINGS)

        assert len(sentences) == 2
        assert sentences[0].episode_id == "ep100"
        assert sentences[0].sentence_index == 0
        assert sentences[0].official_text == "The government announced new policies."
        assert avg_wer == 0.0

    def test_missing_official_raises(self, tmp_path):
        """Missing official transcript should raise FileNotFoundError."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        # Only create whisper, no official
        whisper_data = {"episode_id": "ep200", "segments": []}
        with open(transcript_dir / "ep200_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            with pytest.raises(
                FileNotFoundError, match="Official transcript not found"
            ):
                compare_episode("ep200", settings=SETTINGS)

    def test_missing_whisper_raises(self, tmp_path):
        """Missing whisper transcript should raise FileNotFoundError."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        # Only create official, no whisper
        official_data = {"episode_id": "ep300", "sentences": ["Hello."]}
        with open(transcript_dir / "ep300_official.json", "w") as f:
            json.dump(official_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            with pytest.raises(FileNotFoundError, match="Whisper transcript not found"):
                compare_episode("ep300", settings=SETTINGS)

    def test_avg_wer_calculation(self, tmp_path):
        """Average WER should be the mean across all sentences."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        official_data = {
            "sentences": ["hello world", "foo bar"],
        }
        # Whisper gets first right, second wrong
        whisper_data = {
            "segments": [
                {"text": "hello world", "start": 0.0, "end": 1.0},
                {"text": "baz qux", "start": 1.0, "end": 2.0},
            ],
        }

        with open(transcript_dir / "ep400_official.json", "w") as f:
            json.dump(official_data, f)
        with open(transcript_dir / "ep400_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            sentences, avg_wer = compare_episode("ep400", settings=SETTINGS)

        # First sentence: WER=0, Second: WER=1.0. Average = 0.5
        assert avg_wer == pytest.approx(0.5)

    def test_empty_sentences(self, tmp_path):
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        official_data = {"sentences": []}
        whisper_data = {"segments": []}

        with open(transcript_dir / "ep500_official.json", "w") as f:
            json.dump(official_data, f)
        with open(transcript_dir / "ep500_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            sentences, avg_wer = compare_episode("ep500", settings=SETTINGS)

        assert sentences == []
        assert avg_wer == 0.0

    @patch("src.comparator.load_settings")
    def test_loads_settings_when_none(self, mock_load_settings, tmp_path):
        """When settings=None, load_settings() should be called."""
        mock_load_settings.return_value = SETTINGS

        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        official_data = {"sentences": ["test"]}
        whisper_data = {"segments": [{"text": "test", "start": 0, "end": 1}]}

        with open(transcript_dir / "epnone_official.json", "w") as f:
            json.dump(official_data, f)
        with open(transcript_dir / "epnone_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            compare_episode("epnone", settings=None)

        mock_load_settings.assert_called_once()


# ---------------------------------------------------------------------------
# compare_all
# ---------------------------------------------------------------------------


class TestCompareAll:
    def test_batch_processing(self, tmp_path):
        """Multiple episodes: one succeeds, one skipped (missing file)."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        # ep_ok has both files
        official_data = {"sentences": ["Hello."]}
        whisper_data = {"segments": [{"text": "Hello.", "start": 0, "end": 1}]}

        with open(transcript_dir / "ep_ok_official.json", "w") as f:
            json.dump(official_data, f)
        with open(transcript_dir / "ep_ok_whisper.json", "w") as f:
            json.dump(whisper_data, f)

        # ep_missing has no files at all

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            results = compare_all(["ep_ok", "ep_missing"], settings=SETTINGS)

        assert len(results) == 2

        ok_result = results[0]
        assert ok_result["episode_id"] == "ep_ok"
        assert ok_result["status"] == "done"
        assert len(ok_result["sentences"]) == 1

        missing_result = results[1]
        assert missing_result["episode_id"] == "ep_missing"
        assert missing_result["status"] == "skipped"
        assert "error" in missing_result

    def test_empty_list(self, tmp_path):
        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            results = compare_all([], settings=SETTINGS)
        assert results == []

    @patch("src.comparator.load_settings")
    def test_loads_settings_when_none(self, mock_load_settings, tmp_path):
        mock_load_settings.return_value = SETTINGS

        with patch.object(comparator_module, "_PROJECT_ROOT", tmp_path):
            results = compare_all(["nonexistent"], settings=None)

        mock_load_settings.assert_called_once()
        assert len(results) == 1
        assert results[0]["status"] == "skipped"
