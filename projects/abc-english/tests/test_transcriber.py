"""Unit tests for src/transcriber.py.

All Whisper model interactions are mocked — no real model loading or
audio transcription occurs.  File I/O uses pytest's tmp_path fixture.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Mock the whisper package before importing src.transcriber so the
# top-level ``import whisper`` inside the module succeeds even when
# whisper is not installed in the test environment.
_mock_whisper_module = MagicMock()
_mock_whisper_module.Whisper = MagicMock  # type annotation reference
sys.modules.setdefault("whisper", _mock_whisper_module)

import src.transcriber as transcriber_module  # noqa: E402

from src.transcriber import (  # noqa: E402
    load_model,
    save_whisper_transcript,
    transcribe_all,
    transcribe_audio,
    transcribe_episode,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

SETTINGS = {
    "whisper": {
        "model": "base",
        "device": "cpu",
    },
    "data": {
        "audio_dir": "data/audio",
        "transcript_dir": "data/transcripts",
    },
}


def _reset_singleton():
    """Reset module-level model cache between tests."""
    transcriber_module._model = None
    transcriber_module._model_name = None


def _patch_project_root(tmp_path):
    """Patch Path(__file__).resolve().parent.parent to tmp_path for transcriber."""
    real_path = Path

    class _PatchedPath(type(real_path())):
        def resolve(self, strict=False):
            if str(self) == str(real_path(transcriber_module.__file__)):
                return real_path(tmp_path / "src" / "transcriber.py")
            return super().resolve(strict=strict)

    return patch.object(transcriber_module, "Path", _PatchedPath)


# ---------------------------------------------------------------------------
# load_model
# ---------------------------------------------------------------------------


class TestLoadModel:
    def setup_method(self):
        _reset_singleton()

    def teardown_method(self):
        _reset_singleton()

    @patch("src.transcriber.whisper")
    def test_loads_model_with_settings(self, mock_whisper):
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model

        result = load_model(SETTINGS)

        mock_whisper.load_model.assert_called_once_with("base", device="cpu")
        assert result is fake_model

    @patch("src.transcriber.whisper")
    def test_singleton_caching(self, mock_whisper):
        """Calling load_model twice with same model name should load only once."""
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model

        result1 = load_model(SETTINGS)
        result2 = load_model(SETTINGS)

        assert mock_whisper.load_model.call_count == 1
        assert result1 is result2

    @patch("src.transcriber.whisper")
    def test_reloads_on_different_model(self, mock_whisper):
        """Switching model name should trigger a reload."""
        model_a = MagicMock()
        model_b = MagicMock()
        mock_whisper.load_model.side_effect = [model_a, model_b]

        result_a = load_model(SETTINGS)

        settings_small = {**SETTINGS, "whisper": {"model": "small", "device": "cpu"}}
        result_b = load_model(settings_small)

        assert mock_whisper.load_model.call_count == 2
        assert result_a is model_a
        assert result_b is model_b

    @patch("src.transcriber.whisper")
    def test_default_model_name(self, mock_whisper):
        """Settings missing whisper.model should default to 'base'."""
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model

        load_model({"whisper": {}})
        mock_whisper.load_model.assert_called_once_with("base", device="cpu")


# ---------------------------------------------------------------------------
# transcribe_audio
# ---------------------------------------------------------------------------


class TestTranscribeAudio:
    def test_normal_transcription(self):
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": " The government has announced new policies. ",
            "segments": [
                {"text": " The government has announced", "start": 0.0, "end": 2.5},
                {"text": " new policies.", "start": 2.5, "end": 4.0},
            ],
        }

        result = transcribe_audio("/fake/audio.mp3", mock_model)

        assert result["full_text"] == "The government has announced new policies."
        assert len(result["segments"]) == 2
        assert result["segments"][0]["text"] == "The government has announced"
        assert result["segments"][0]["start"] == 0.0
        assert result["segments"][0]["end"] == 2.5

    def test_empty_segments_filtered(self):
        """Segments with empty or whitespace-only text should be excluded."""
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "Hello world.",
            "segments": [
                {"text": "Hello world.", "start": 0.0, "end": 1.0},
                {"text": "   ", "start": 1.0, "end": 1.5},
                {"text": "", "start": 1.5, "end": 2.0},
            ],
        }

        result = transcribe_audio("/fake/audio.mp3", mock_model)

        assert len(result["segments"]) == 1
        assert result["segments"][0]["text"] == "Hello world."

    def test_timestamps_rounded(self):
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "Test.",
            "segments": [
                {"text": "Test.", "start": 0.123456, "end": 1.987654},
            ],
        }

        result = transcribe_audio("/fake/audio.mp3", mock_model)

        assert result["segments"][0]["start"] == 0.12
        assert result["segments"][0]["end"] == 1.99

    def test_no_segments(self):
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "text": "No segments here.",
            "segments": [],
        }

        result = transcribe_audio("/fake/audio.mp3", mock_model)

        assert result["full_text"] == "No segments here."
        assert result["segments"] == []

    def test_passes_language_en(self):
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "", "segments": []}

        transcribe_audio("/fake/audio.mp3", mock_model)

        mock_model.transcribe.assert_called_once_with("/fake/audio.mp3", language="en")


# ---------------------------------------------------------------------------
# save_whisper_transcript
# ---------------------------------------------------------------------------


class TestSaveWhisperTranscript:
    def test_creates_json_file(self, tmp_path):
        result_data = {
            "full_text": "Hello world.",
            "segments": [
                {"text": "Hello world.", "start": 0.0, "end": 1.5},
            ],
        }

        with _patch_project_root(tmp_path):
            path = save_whisper_transcript("ep001", result_data, SETTINGS)

        out_file = tmp_path / "data" / "transcripts" / "ep001_whisper.json"
        assert out_file.exists()
        assert path == str(out_file)

        with open(out_file) as f:
            saved = json.load(f)

        assert saved["episode_id"] == "ep001"
        assert saved["full_text"] == "Hello world."
        assert len(saved["segments"]) == 1

    def test_creates_directory_if_needed(self, tmp_path):
        """Transcript dir should be auto-created."""
        result_data = {"full_text": "Test.", "segments": []}

        with _patch_project_root(tmp_path):
            save_whisper_transcript("ep002", result_data, SETTINGS)

        out_dir = tmp_path / "data" / "transcripts"
        assert out_dir.is_dir()

    def test_overwrites_existing(self, tmp_path):
        data1 = {"full_text": "First.", "segments": []}
        data2 = {"full_text": "Second.", "segments": []}

        with _patch_project_root(tmp_path):
            save_whisper_transcript("ep003", data1, SETTINGS)
            save_whisper_transcript("ep003", data2, SETTINGS)

        out_file = tmp_path / "data" / "transcripts" / "ep003_whisper.json"
        with open(out_file) as f:
            saved = json.load(f)
        assert saved["full_text"] == "Second."


# ---------------------------------------------------------------------------
# transcribe_episode
# ---------------------------------------------------------------------------


class TestTranscribeEpisode:
    def setup_method(self):
        _reset_singleton()

    def teardown_method(self):
        _reset_singleton()

    @patch("src.transcriber.whisper")
    def test_normal_flow(self, mock_whisper, tmp_path):
        """Full transcription: load model, transcribe audio, save JSON."""
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model
        fake_model.transcribe.return_value = {
            "text": "Hello from episode.",
            "segments": [
                {"text": "Hello from episode.", "start": 0.0, "end": 2.0},
            ],
        }

        # Create the audio file
        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True)
        (audio_dir / "ep100.mp3").write_bytes(b"fake_audio")

        with _patch_project_root(tmp_path):
            result = transcribe_episode("ep100", SETTINGS)

        assert result["episode_id"] == "ep100"
        assert result["full_text"] == "Hello from episode."
        assert result["skipped"] is False
        assert result["path"] != ""

        # Verify saved file
        saved_path = tmp_path / "data" / "transcripts" / "ep100_whisper.json"
        assert saved_path.exists()

    def test_skip_existing_transcript(self, tmp_path):
        """If whisper transcript already exists, skip transcription."""
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)

        existing_data = {
            "episode_id": "ep200",
            "full_text": "Already transcribed.",
            "segments": [{"text": "Already transcribed.", "start": 0.0, "end": 1.0}],
        }
        existing_path = transcript_dir / "ep200_whisper.json"
        with open(existing_path, "w") as f:
            json.dump(existing_data, f)

        with _patch_project_root(tmp_path):
            result = transcribe_episode("ep200", SETTINGS)

        assert result["skipped"] is True
        assert result["full_text"] == "Already transcribed."
        assert result["path"] == str(existing_path)

    def test_audio_not_found_raises(self, tmp_path):
        """Missing audio file should raise FileNotFoundError."""
        # No audio file created
        with _patch_project_root(tmp_path):
            with pytest.raises(FileNotFoundError, match="Audio file not found"):
                transcribe_episode("ep_missing", SETTINGS)


# ---------------------------------------------------------------------------
# transcribe_all
# ---------------------------------------------------------------------------


class TestTranscribeAll:
    def setup_method(self):
        _reset_singleton()

    def teardown_method(self):
        _reset_singleton()

    @patch("src.transcriber.whisper")
    def test_batch_processing(self, mock_whisper, tmp_path):
        """Multiple episodes: one done, one skipped (existing)."""
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model
        fake_model.transcribe.return_value = {
            "text": "New episode.",
            "segments": [{"text": "New episode.", "start": 0.0, "end": 1.0}],
        }

        # ep_new: audio file exists, no whisper transcript
        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True)
        (audio_dir / "ep_new.mp3").write_bytes(b"audio_data")

        # ep_existing: whisper transcript already exists
        transcript_dir = tmp_path / "data" / "transcripts"
        transcript_dir.mkdir(parents=True)
        existing_data = {
            "episode_id": "ep_existing",
            "full_text": "Old.",
            "segments": [],
        }
        with open(transcript_dir / "ep_existing_whisper.json", "w") as f:
            json.dump(existing_data, f)

        with _patch_project_root(tmp_path):
            results = transcribe_all(["ep_new", "ep_existing"], settings=SETTINGS)

        assert len(results) == 2

        new_result = results[0]
        assert new_result["episode_id"] == "ep_new"
        assert new_result["skipped"] is False
        assert new_result["full_text"] == "New episode."

        existing_result = results[1]
        assert existing_result["episode_id"] == "ep_existing"
        assert existing_result["skipped"] is True

    @patch("src.transcriber.whisper")
    def test_missing_audio_counted_as_error(self, mock_whisper, tmp_path):
        """Episode with no audio file should appear in results with error."""
        fake_model = MagicMock()
        mock_whisper.load_model.return_value = fake_model

        with _patch_project_root(tmp_path):
            results = transcribe_all(["ep_no_audio"], settings=SETTINGS)

        assert len(results) == 1
        assert "error" in results[0]
        assert results[0]["full_text"] == ""

    @patch("src.transcriber.load_settings")
    def test_loads_settings_when_none(self, mock_load_settings, tmp_path):
        """When settings=None, load_settings() should be called."""
        mock_load_settings.return_value = SETTINGS

        with _patch_project_root(tmp_path):
            # Will fail at audio lookup, but we only care that settings were loaded
            results = transcribe_all(["ep_test"], settings=None)

        mock_load_settings.assert_called_once()

    def test_empty_list(self, tmp_path):
        with _patch_project_root(tmp_path):
            results = transcribe_all([], settings=SETTINGS)
        assert results == []
