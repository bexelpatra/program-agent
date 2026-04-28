"""Unit tests for src/cli.py.

All pipeline functions are mocked — no real data processing, network, or ES calls.
"""

import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

# Install a mock ``whisper`` package so that ``src.transcriber`` can be imported
# even when the real whisper library is not installed.
if "whisper" not in sys.modules:
    try:
        import whisper  # noqa: F401
    except ImportError:
        _mock_whisper = MagicMock()
        _mock_whisper.__name__ = "whisper"
        _mock_whisper.__package__ = "whisper"
        _mock_whisper.__path__ = []
        sys.modules["whisper"] = _mock_whisper

from src.cli import cli, _scan_episode_ids


# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

SETTINGS = {
    "crawling": {"base_url": "https://example.com"},
    "data": {"transcript_dir": "data/transcripts"},
    "elasticsearch": {"host": "localhost", "port": 9200},
}


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_settings():
    """Patch _load_settings (module-level helper) to return SETTINGS."""
    with patch("src.cli._load_settings", return_value=SETTINGS) as m:
        yield m


@pytest.fixture
def mock_transcript_dir(tmp_path):
    """Patch _get_transcript_dir to return a tmp_path-based directory."""
    transcript_dir = tmp_path / "transcripts"
    transcript_dir.mkdir()
    with patch("src.cli._get_transcript_dir", return_value=transcript_dir):
        yield transcript_dir


# ---------------------------------------------------------------------------
# cli --help
# ---------------------------------------------------------------------------


class TestCLIHelp:
    def test_help_shows_commands(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        # All 9 sub-commands should appear
        for cmd in [
            "collect",
            "transcribe",
            "compare",
            "analyze",
            "llm-analyze",
            "load",
            "run-all",
            "init-indices",
            "delete-indices",
        ]:
            assert cmd in result.output


# ---------------------------------------------------------------------------
# collect
# ---------------------------------------------------------------------------


class TestCollect:
    def test_collect_summary(self, runner, mock_settings):
        ep1 = SimpleNamespace(has_transcript=True)
        ep2 = SimpleNamespace(has_transcript=False)
        ep3 = SimpleNamespace(has_transcript=True)
        with patch("src.collector.collect_all", return_value=[ep1, ep2, ep3]):
            result = runner.invoke(cli, ["collect"])
        assert result.exit_code == 0
        assert "3 episodes found" in result.output
        assert "2 with transcript" in result.output


# ---------------------------------------------------------------------------
# transcribe
# ---------------------------------------------------------------------------


class TestTranscribe:
    def test_transcribe_summary(self, runner, mock_settings, mock_transcript_dir):
        # Create official transcript files so _scan_episode_ids finds them
        (mock_transcript_dir / "ep001_official.json").write_text("{}")
        (mock_transcript_dir / "ep002_official.json").write_text("{}")

        mock_results = [
            {"status": "done", "skipped": False},
            {"skipped": True},
        ]
        with patch("src.transcriber.transcribe_all", return_value=mock_results):
            result = runner.invoke(cli, ["transcribe"])
        assert result.exit_code == 0
        assert "2 episodes to transcribe" in result.output
        assert "1 processed" in result.output
        assert "1 skipped" in result.output

    def test_transcribe_no_episodes(self, runner, mock_settings, mock_transcript_dir):
        # Empty directory — no official transcripts
        result = runner.invoke(cli, ["transcribe"])
        assert result.exit_code == 0
        assert "No episodes with official transcripts found" in result.output


# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------


class TestCompare:
    def test_compare_both_transcripts(self, runner, mock_settings, mock_transcript_dir):
        # ep001 has both, ep002 only official, ep003 only whisper
        (mock_transcript_dir / "ep001_official.json").write_text("{}")
        (mock_transcript_dir / "ep001_whisper.json").write_text("{}")
        (mock_transcript_dir / "ep002_official.json").write_text("{}")
        (mock_transcript_dir / "ep003_whisper.json").write_text("{}")

        mock_results = [{"status": "done"}]
        with patch("src.comparator.compare_all", return_value=mock_results) as mock_cmp:
            result = runner.invoke(cli, ["compare"])

        assert result.exit_code == 0
        # Only ep001 has both transcripts
        assert "Comparing 1 episodes" in result.output
        mock_cmp.assert_called_once()
        called_ids = mock_cmp.call_args[0][0]
        assert called_ids == ["ep001"]

    def test_compare_no_episodes(self, runner, mock_settings, mock_transcript_dir):
        result = runner.invoke(cli, ["compare"])
        assert result.exit_code == 0
        assert (
            "No episodes with both official and whisper transcripts found"
            in result.output
        )


# ---------------------------------------------------------------------------
# analyze
# ---------------------------------------------------------------------------


class TestAnalyze:
    def test_analyze_summary(self, runner, mock_settings, mock_transcript_dir):
        (mock_transcript_dir / "ep001_official.json").write_text("{}")
        vocab_items = [{"word": "hello"}, {"word": "world"}, {"word": "news"}]
        with patch("src.analyzer.analyze_all", return_value=vocab_items):
            result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0
        assert "3 unique vocabulary items extracted" in result.output

    def test_analyze_no_episodes(self, runner, mock_settings, mock_transcript_dir):
        result = runner.invoke(cli, ["analyze"])
        assert result.exit_code == 0
        assert "No episodes found" in result.output


# ---------------------------------------------------------------------------
# llm-analyze
# ---------------------------------------------------------------------------


class TestLLMAnalyze:
    def test_llm_analyze_summary(self, runner, mock_settings, mock_transcript_dir):
        (mock_transcript_dir / "ep001_official.json").write_text("{}")
        (mock_transcript_dir / "ep002_official.json").write_text("{}")

        with patch(
            "src.llm_analyzer.detect_expressions_for_episode",
            return_value=[{"expr": "break a leg"}],
        ) as mock_detect, patch(
            "src.llm_analyzer.classify_vocabulary_for_episode",
            return_value=[{"word": "classified"}],
        ) as mock_classify:
            result = runner.invoke(cli, ["llm-analyze"])

        assert result.exit_code == 0
        assert "2 expressions detected" in result.output
        assert "2 vocabulary items classified" in result.output
        assert mock_detect.call_count == 2
        assert mock_classify.call_count == 2

    def test_llm_analyze_no_episodes(self, runner, mock_settings, mock_transcript_dir):
        result = runner.invoke(cli, ["llm-analyze"])
        assert result.exit_code == 0
        assert "No episodes found" in result.output

    def test_llm_analyze_error_handling(
        self, runner, mock_settings, mock_transcript_dir
    ):
        (mock_transcript_dir / "ep001_official.json").write_text("{}")

        with patch(
            "src.llm_analyzer.detect_expressions_for_episode",
            side_effect=RuntimeError("API error"),
        ), patch(
            "src.llm_analyzer.classify_vocabulary_for_episode",
            side_effect=RuntimeError("API error"),
        ):
            result = runner.invoke(cli, ["llm-analyze"])

        assert result.exit_code == 0
        assert "0 expressions detected" in result.output
        assert "0 vocabulary items classified" in result.output


# ---------------------------------------------------------------------------
# init-indices
# ---------------------------------------------------------------------------


class TestInitIndices:
    def test_init_indices_output(self, runner, mock_settings):
        mock_results = {
            "episodes": {"index_name": "abc_episodes", "created": True},
            "vocabulary": {"index_name": "abc_vocabulary", "created": False},
        }
        with patch("src.models.create_indices", return_value=mock_results):
            result = runner.invoke(cli, ["init-indices"])

        assert result.exit_code == 0
        assert "abc_episodes (created)" in result.output
        assert "abc_vocabulary (already exists)" in result.output
        assert "Index initialization complete" in result.output


# ---------------------------------------------------------------------------
# delete-indices
# ---------------------------------------------------------------------------


class TestDeleteIndices:
    def test_delete_indices_confirmed(self, runner, mock_settings):
        mock_results = {
            "episodes": {"index_name": "abc_episodes", "deleted": True},
            "vocabulary": {"index_name": "abc_vocabulary", "deleted": False},
        }
        with patch("src.models.delete_indices", return_value=mock_results):
            result = runner.invoke(cli, ["delete-indices"], input="y\n")

        assert result.exit_code == 0
        assert "abc_episodes (deleted)" in result.output
        assert "abc_vocabulary (not found)" in result.output
        assert "Index deletion complete" in result.output

    def test_delete_indices_aborted(self, runner, mock_settings):
        result = runner.invoke(cli, ["delete-indices"], input="n\n")
        assert result.exit_code == 0
        assert "Aborted" in result.output


# ---------------------------------------------------------------------------
# _scan_episode_ids
# ---------------------------------------------------------------------------


class TestScanEpisodeIds:
    def test_scan_finds_matching_files(self, tmp_path):
        (tmp_path / "ep001_official.json").write_text("{}")
        (tmp_path / "ep002_official.json").write_text("{}")
        (tmp_path / "ep003_whisper.json").write_text("{}")
        (tmp_path / "unrelated.json").write_text("{}")

        ids = _scan_episode_ids(tmp_path, "official")
        assert ids == ["ep001", "ep002"]

    def test_scan_empty_dir(self, tmp_path):
        ids = _scan_episode_ids(tmp_path, "official")
        assert ids == []

    def test_scan_nonexistent_dir(self, tmp_path):
        ids = _scan_episode_ids(tmp_path / "nonexistent", "official")
        assert ids == []

    def test_scan_complex_episode_id(self, tmp_path):
        """Episode IDs may contain underscores themselves."""
        (tmp_path / "106551254_official.json").write_text("{}")
        (tmp_path / "my_episode_99_whisper.json").write_text("{}")

        ids = _scan_episode_ids(tmp_path, "official")
        assert ids == ["106551254"]

        ids = _scan_episode_ids(tmp_path, "whisper")
        assert ids == ["my_episode_99"]
