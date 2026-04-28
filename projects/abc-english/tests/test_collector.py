"""Unit tests for src/collector.py.

All HTTP requests are mocked — no real network calls are made.
File I/O uses pytest's tmp_path fixture.
"""

import json
import os
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest
import requests

import src.collector as collector_module

from src.collector import (
    _build_episode_url,
    _deep_get,
    _extract_audio_url,
    _extract_episode_id,
    _extract_items_from_next_data,
    _extract_next_data,
    _request_with_retry,
    collect_all,
    download_mp3,
    fetch_episode_detail,
    fetch_episode_list,
    parse_transcript,
    save_transcript,
)


# ---------------------------------------------------------------------------
# Shared fixtures and helpers
# ---------------------------------------------------------------------------

SETTINGS = {
    "crawling": {
        "base_url": "https://www.abc.net.au",
        "program_url": "https://www.abc.net.au/listen/programs/abc-news-daily",
        "request_delay": 0,  # no delay in tests
        "request_timeout": 5,
        "user_agent": "TestAgent/1.0",
        "max_retries": 2,
    },
    "data": {
        "audio_dir": "data/audio",
        "transcript_dir": "data/transcripts",
    },
}

# The real Path class, saved before any patching.
_RealPath = Path

# Collector module's __file__ path (used to detect Path(__file__) calls).
_COLLECTOR_FILE = collector_module.__file__


@contextmanager
def _patch_project_root(tmp_path):
    """Context manager that makes collector think its project root is *tmp_path*.

    Both ``save_transcript`` and ``download_mp3`` compute project root as
    ``Path(__file__).resolve().parent.parent``.  We intercept only that call
    and redirect it to *tmp_path* while leaving all other ``Path`` usage intact.
    """
    real_path = _RealPath

    class _PatchedPath(type(real_path())):
        """Subclass that overrides resolve() only for the collector __file__."""

        def resolve(self, strict=False):
            if str(self) == str(real_path(_COLLECTOR_FILE)):
                # Return a fake resolved path whose .parent.parent == tmp_path
                # We need: fake.parent.parent == tmp_path
                # So fake = tmp_path / "src" / "collector.py"
                return real_path(tmp_path / "src" / "collector.py")
            return super().resolve(strict=strict)

    with patch.object(collector_module, "Path", _PatchedPath):
        yield


def _make_next_data_html(next_data: dict) -> str:
    """Wrap a __NEXT_DATA__ dict in a minimal HTML page."""
    blob = json.dumps(next_data)
    return (
        "<html><head>"
        f'<script id="__NEXT_DATA__" type="application/json">{blob}</script>'
        "</head><body></body></html>"
    )


def _make_episode_page_html(
    next_data: dict,
    has_transcript: bool = True,
    transcript_text: str = "Hello world. How are you? I am fine!",
) -> str:
    """Build a full episode detail HTML page."""
    blob = json.dumps(next_data)
    transcript_div = ""
    if has_transcript:
        transcript_div = f'<div id="transcript"><p>{transcript_text}</p></div>'
    return (
        "<html><head>"
        f'<script id="__NEXT_DATA__" type="application/json">{blob}</script>'
        f"</head><body>{transcript_div}</body></html>"
    )


def _mock_response(text: str = "", status_code: int = 200, headers: dict = None):
    """Create a mock requests.Response."""
    resp = MagicMock(spec=requests.Response)
    resp.text = text
    resp.status_code = status_code
    resp.headers = headers or {}
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(
            f"{status_code} Error", response=resp
        )
    return resp


# ---------------------------------------------------------------------------
# _extract_next_data
# ---------------------------------------------------------------------------


class TestExtractNextData:
    def test_valid_html(self):
        data = {"props": {"pageProps": {"hello": "world"}}}
        html = _make_next_data_html(data)
        result = _extract_next_data(html)
        assert result == data

    def test_missing_tag_raises(self):
        html = "<html><body>No script here</body></html>"
        with pytest.raises(ValueError, match="__NEXT_DATA__"):
            _extract_next_data(html)

    def test_empty_script_raises(self):
        html = '<html><script id="__NEXT_DATA__"></script></html>'
        with pytest.raises(ValueError, match="__NEXT_DATA__"):
            _extract_next_data(html)


# ---------------------------------------------------------------------------
# _extract_items_from_next_data
# ---------------------------------------------------------------------------


class TestExtractItemsFromNextData:
    def test_first_path(self):
        data = {
            "props": {
                "pageProps": {
                    "data": {
                        "program": {"episodes": {"items": [{"id": "1"}, {"id": "2"}]}}
                    }
                }
            }
        }
        assert len(_extract_items_from_next_data(data)) == 2

    def test_second_path(self):
        data = {"props": {"pageProps": {"data": {"items": [{"id": "1"}]}}}}
        assert len(_extract_items_from_next_data(data)) == 1

    def test_third_path(self):
        data = {"props": {"pageProps": {"episodes": [{"id": "a"}]}}}
        assert len(_extract_items_from_next_data(data)) == 1

    def test_empty_returns_empty(self):
        assert _extract_items_from_next_data({}) == []
        assert _extract_items_from_next_data({"props": {}}) == []

    def test_empty_list_returns_empty(self):
        data = {"props": {"pageProps": {"episodes": []}}}
        assert _extract_items_from_next_data(data) == []


# ---------------------------------------------------------------------------
# _extract_episode_id
# ---------------------------------------------------------------------------


class TestExtractEpisodeId:
    def test_direct_id(self):
        assert _extract_episode_id({"id": "12345"}) == "12345"

    def test_episodeId_key(self):
        assert _extract_episode_id({"episodeId": "99"}) == "99"

    def test_from_link_url(self):
        item = {"link": "/listen/programs/abc-news-daily/slug/12345"}
        assert _extract_episode_id(item) == "12345"

    def test_no_id_returns_none(self):
        assert _extract_episode_id({"title": "no id here"}) is None

    def test_integer_id(self):
        assert _extract_episode_id({"id": 42}) == "42"


# ---------------------------------------------------------------------------
# _build_episode_url
# ---------------------------------------------------------------------------


class TestBuildEpisodeUrl:
    def test_full_url_passthrough(self):
        item = {"link": "https://example.com/ep/1"}
        assert (
            _build_episode_url(item, "https://abc.net.au") == "https://example.com/ep/1"
        )

    def test_relative_url(self):
        item = {"link": "/listen/programs/abc-news-daily/slug/123"}
        assert _build_episode_url(item, "https://abc.net.au") == (
            "https://abc.net.au/listen/programs/abc-news-daily/slug/123"
        )

    def test_from_slug_and_id(self):
        item = {"slug": "my-episode", "id": "999"}
        url = _build_episode_url(item, "https://abc.net.au")
        assert "my-episode" in url
        assert "999" in url

    def test_empty_item(self):
        assert _build_episode_url({}, "https://abc.net.au") == ""


# ---------------------------------------------------------------------------
# _extract_audio_url
# ---------------------------------------------------------------------------


class TestExtractAudioUrl:
    def test_direct_key(self):
        assert _extract_audio_url({"audioUrl": "https://x.mp3"}) == "https://x.mp3"

    def test_nested_media(self):
        item = {"media": {"url": "https://y.mp3"}}
        assert _extract_audio_url(item) == "https://y.mp3"

    def test_no_audio(self):
        assert _extract_audio_url({"title": "no audio"}) == ""


# ---------------------------------------------------------------------------
# _deep_get
# ---------------------------------------------------------------------------


class TestDeepGet:
    def test_camel_case(self):
        assert (
            _deep_get({"publishedDate": "2024-01-01"}, "publishedDate") == "2024-01-01"
        )

    def test_snake_case_fallback(self):
        assert (
            _deep_get({"published_date": "2024-01-01"}, "publishedDate") == "2024-01-01"
        )

    def test_missing_returns_default(self):
        assert _deep_get({}, "foo", default="bar") == "bar"


# ---------------------------------------------------------------------------
# _request_with_retry
# ---------------------------------------------------------------------------


class TestRequestWithRetry:
    @patch("src.collector._make_session")
    def test_success_first_try(self, _):
        session = MagicMock()
        resp = _mock_response("ok")
        session.get.return_value = resp
        result = _request_with_retry(session, "http://test.com", SETTINGS)
        assert result is resp
        assert session.get.call_count == 1

    @patch("src.collector.time.sleep")
    def test_retry_then_success(self, mock_sleep):
        session = MagicMock()
        fail_resp = _mock_response("fail", 500)
        ok_resp = _mock_response("ok")
        session.get.side_effect = [
            requests.RequestException("fail"),
            ok_resp,
        ]
        result = _request_with_retry(session, "http://test.com", SETTINGS)
        assert result is ok_resp
        assert session.get.call_count == 2
        mock_sleep.assert_called_once()

    @patch("src.collector.time.sleep")
    def test_all_retries_exhausted(self, mock_sleep):
        session = MagicMock()
        session.get.side_effect = requests.RequestException("always fail")
        with pytest.raises(requests.RequestException, match="always fail"):
            _request_with_retry(session, "http://test.com", SETTINGS)
        assert session.get.call_count == 2  # max_retries=2


# ---------------------------------------------------------------------------
# fetch_episode_list
# ---------------------------------------------------------------------------


class TestFetchEpisodeList:
    @patch("src.collector.time.sleep")
    @patch("src.collector._request_with_retry")
    def test_single_page(self, mock_req, mock_sleep):
        next_data = {
            "props": {
                "pageProps": {
                    "data": {
                        "program": {
                            "episodes": {
                                "items": [
                                    {
                                        "id": "100",
                                        "title": "Episode One",
                                        "description": "Desc",
                                        "publishedDate": "2024-01-01",
                                        "duration": 900,
                                        "link": "/listen/programs/abc-news-daily/ep/100",
                                        "audioUrl": "https://audio.mp3",
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
        html = _make_next_data_html(next_data)

        # First call returns items, second call returns empty
        empty_data = {
            "props": {"pageProps": {"data": {"program": {"episodes": {"items": []}}}}}
        }
        empty_html = _make_next_data_html(empty_data)

        resp1 = _mock_response(html)
        resp2 = _mock_response(empty_html)
        mock_req.side_effect = [resp1, resp2]

        result = fetch_episode_list(SETTINGS)
        assert len(result) == 1
        assert result[0]["episode_id"] == "100"
        assert result[0]["title"] == "Episode One"

    @patch("src.collector.time.sleep")
    @patch("src.collector._request_with_retry")
    def test_deduplication(self, mock_req, mock_sleep):
        """Same episode appearing on two pages should be deduplicated."""
        items = [
            {
                "id": "100",
                "title": "Ep",
                "link": "/ep/100",
                "audioUrl": "",
            }
        ]
        next_data = {
            "props": {
                "pageProps": {"data": {"program": {"episodes": {"items": items}}}}
            }
        }
        html = _make_next_data_html(next_data)
        resp = _mock_response(html)
        # Both pages return the same episode -> new_count=0 on second page
        mock_req.side_effect = [resp, resp]

        result = fetch_episode_list(SETTINGS)
        assert len(result) == 1

    @patch("src.collector.time.sleep")
    @patch("src.collector._request_with_retry")
    def test_empty_first_page(self, mock_req, mock_sleep):
        empty_data = {"props": {"pageProps": {"data": {"items": []}}}}
        resp = _mock_response(_make_next_data_html(empty_data))
        mock_req.return_value = resp
        result = fetch_episode_list(SETTINGS)
        assert result == []


# ---------------------------------------------------------------------------
# fetch_episode_detail
# ---------------------------------------------------------------------------


class TestFetchEpisodeDetail:
    @patch("src.collector._request_with_retry")
    @patch("src.collector._make_session")
    def test_with_transcript(self, mock_session, mock_req):
        next_data = {
            "props": {
                "pageProps": {
                    "data": {
                        "episode": {
                            "id": "200",
                            "title": "Detail Ep",
                            "description": "A desc",
                            "publishedDate": "2024-03-01",
                            "duration": 600,
                            "audioUrl": "https://audio2.mp3",
                        }
                    }
                }
            }
        }
        html = _make_episode_page_html(next_data, has_transcript=True)
        mock_req.return_value = _mock_response(html)

        result = fetch_episode_detail("https://abc.net.au/ep/200", SETTINGS)
        assert result["has_transcript"] is True
        assert result["episode_id"] == "200"
        assert result["title"] == "Detail Ep"
        assert "_html" in result

    @patch("src.collector._request_with_retry")
    @patch("src.collector._make_session")
    def test_without_transcript(self, mock_session, mock_req):
        next_data = {
            "props": {
                "pageProps": {"data": {"episode": {"id": "201", "title": "No Trans"}}}
            }
        }
        html = _make_episode_page_html(next_data, has_transcript=False)
        mock_req.return_value = _mock_response(html)

        result = fetch_episode_detail("https://abc.net.au/ep/201", SETTINGS)
        assert result["has_transcript"] is False

    @patch("src.collector._request_with_retry")
    @patch("src.collector._make_session")
    def test_fallback_episode_id_from_url(self, mock_session, mock_req):
        """When __NEXT_DATA__ has no id, fall back to URL parsing."""
        next_data = {"props": {"pageProps": {}}}
        html = _make_episode_page_html(next_data, has_transcript=False)
        mock_req.return_value = _mock_response(html)

        result = fetch_episode_detail("https://abc.net.au/ep/99999", SETTINGS)
        assert result["episode_id"] == "99999"


# ---------------------------------------------------------------------------
# parse_transcript
# ---------------------------------------------------------------------------


class TestParseTranscript:
    def test_normal_transcript(self):
        html = (
            '<html><body><div id="transcript">'
            "<p>Hello world. How are you? I am fine!</p>"
            "</div></body></html>"
        )
        result = parse_transcript(html)
        assert result["full_text"] != ""
        assert len(result["sentences"]) == 3
        assert result["sentences"][0] == "Hello world."
        assert result["sentences"][1] == "How are you?"
        assert result["sentences"][2] == "I am fine!"

    def test_no_transcript_element(self):
        html = "<html><body><p>No transcript</p></body></html>"
        result = parse_transcript(html)
        assert result["full_text"] == ""
        assert result["sentences"] == []

    def test_empty_transcript(self):
        html = '<html><body><div id="transcript">   </div></body></html>'
        result = parse_transcript(html)
        assert result["full_text"] == ""
        assert result["sentences"] == []

    def test_multiple_paragraphs(self):
        html = (
            '<html><body><div id="transcript">'
            "<p>First sentence.</p>"
            "<p>Second sentence.</p>"
            "</div></body></html>"
        )
        result = parse_transcript(html)
        assert len(result["sentences"]) == 2

    def test_whitespace_normalisation(self):
        html = (
            '<html><body><div id="transcript">'
            "<p>  Lots   of   spaces.   Really?  </p>"
            "</div></body></html>"
        )
        result = parse_transcript(html)
        assert "  " not in result["full_text"]


# ---------------------------------------------------------------------------
# save_transcript
# ---------------------------------------------------------------------------


class TestSaveTranscript:
    def test_save_creates_file(self, tmp_path):
        transcript_data = {
            "full_text": "Hello world.",
            "sentences": ["Hello world."],
        }
        settings = {"data": {"transcript_dir": "data/transcripts"}}

        with _patch_project_root(tmp_path):
            result = save_transcript("ep001", transcript_data, settings)

        expected_file = tmp_path / "data" / "transcripts" / "ep001_official.json"
        assert expected_file.exists()

        with open(expected_file) as f:
            saved = json.load(f)
        assert saved["episode_id"] == "ep001"
        assert saved["sentences"] == ["Hello world."]
        assert saved["full_text"] == "Hello world."

    def test_save_overwrites_existing(self, tmp_path):
        """Saving twice with same episode_id should overwrite."""
        settings = {"data": {"transcript_dir": "data/transcripts"}}
        data1 = {"full_text": "First.", "sentences": ["First."]}
        data2 = {"full_text": "Second.", "sentences": ["Second."]}

        with _patch_project_root(tmp_path):
            save_transcript("ep002", data1, settings)
            save_transcript("ep002", data2, settings)

        out_file = tmp_path / "data" / "transcripts" / "ep002_official.json"
        with open(out_file) as f:
            saved = json.load(f)
        assert saved["full_text"] == "Second."


# ---------------------------------------------------------------------------
# download_mp3
# ---------------------------------------------------------------------------


class TestDownloadMp3:
    def test_download_success(self, tmp_path):
        with _patch_project_root(tmp_path), patch(
            "src.collector._make_session"
        ) as mock_session_fn:
            mock_session = MagicMock()
            mock_session_fn.return_value = mock_session

            fake_resp = MagicMock()
            fake_resp.headers = {"content-length": "100"}
            fake_resp.iter_content.return_value = [b"fake_mp3_data"]
            fake_resp.raise_for_status = MagicMock()
            mock_session.get.return_value = fake_resp

            result = download_mp3("ep100", "https://audio.mp3", SETTINGS)

            expected = tmp_path / "data" / "audio" / "ep100.mp3"
            assert expected.exists()
            assert result == str(expected)
            assert expected.read_bytes() == b"fake_mp3_data"

    def test_duplicate_skip(self, tmp_path):
        """If MP3 already exists, skip download."""
        # Pre-create the file
        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        existing = audio_dir / "ep100.mp3"
        existing.write_bytes(b"existing")

        with _patch_project_root(tmp_path), patch(
            "src.collector._make_session"
        ) as mock_session_fn:
            result = download_mp3("ep100", "https://audio.mp3", SETTINGS)
            assert result == str(existing)
            # Session should NOT have been used for download
            mock_session_fn.return_value.get.assert_not_called()

    def test_empty_audio_url(self, tmp_path):
        with _patch_project_root(tmp_path):
            result = download_mp3("ep100", "", SETTINGS)
            assert result == ""

    def test_network_error_cleans_up(self, tmp_path):
        """On download failure, partial .tmp file should be removed."""
        with _patch_project_root(tmp_path), patch(
            "src.collector._make_session"
        ) as mock_session_fn:
            mock_session = MagicMock()
            mock_session_fn.return_value = mock_session

            fake_resp = MagicMock()
            fake_resp.headers = {"content-length": "100"}
            fake_resp.iter_content.side_effect = requests.ConnectionError("broken")
            fake_resp.raise_for_status = MagicMock()
            mock_session.get.return_value = fake_resp

            with pytest.raises(requests.ConnectionError):
                download_mp3("ep_fail", "https://audio.mp3", SETTINGS)

            # tmp file should be cleaned up
            tmp_file = tmp_path / "data" / "audio" / "ep_fail.mp3.tmp"
            assert not tmp_file.exists()
            # Final file should not exist either
            final_file = tmp_path / "data" / "audio" / "ep_fail.mp3"
            assert not final_file.exists()


# ---------------------------------------------------------------------------
# collect_all
# ---------------------------------------------------------------------------


class TestCollectAll:
    @patch("src.collector.time.sleep")
    @patch("src.collector.download_mp3")
    @patch("src.collector.save_transcript")
    @patch("src.collector.parse_transcript")
    @patch("src.collector.fetch_episode_detail")
    @patch("src.collector.fetch_episode_list")
    def test_full_pipeline_with_transcript(
        self,
        mock_list,
        mock_detail,
        mock_parse,
        mock_save,
        mock_download,
        mock_sleep,
    ):
        mock_list.return_value = [
            {
                "episode_id": "300",
                "title": "Full Pipeline Ep",
                "description": "Desc",
                "published_date": "2024-05-01",
                "duration_seconds": 900,
                "url": "https://abc.net.au/ep/300",
                "audio_url": "https://audio.mp3",
            }
        ]
        mock_detail.return_value = {
            "url": "https://abc.net.au/ep/300",
            "has_transcript": True,
            "episode_id": "300",
            "title": "Full Pipeline Ep",
            "description": "Desc",
            "published_date": "2024-05-01",
            "duration_seconds": 900,
            "audio_url": "https://audio.mp3",
            "_html": '<div id="transcript">Hello.</div>',
        }
        mock_parse.return_value = {
            "full_text": "Hello.",
            "sentences": ["Hello."],
        }
        mock_save.return_value = "/tmp/transcripts/300_official.json"
        mock_download.return_value = "/tmp/audio/300.mp3"

        episodes = collect_all(SETTINGS)

        assert len(episodes) == 1
        ep = episodes[0]
        assert ep.episode_id == "300"
        assert ep.has_transcript is True
        assert ep.official_transcript == "Hello."
        mock_parse.assert_called_once()
        mock_save.assert_called_once()
        mock_download.assert_called_once()

    @patch("src.collector.time.sleep")
    @patch("src.collector.download_mp3")
    @patch("src.collector.save_transcript")
    @patch("src.collector.parse_transcript")
    @patch("src.collector.fetch_episode_detail")
    @patch("src.collector.fetch_episode_list")
    def test_skip_episode_without_transcript(
        self,
        mock_list,
        mock_detail,
        mock_parse,
        mock_save,
        mock_download,
        mock_sleep,
    ):
        mock_list.return_value = [
            {
                "episode_id": "301",
                "title": "No Trans Ep",
                "description": "",
                "published_date": "2024-06-01",
                "duration_seconds": 600,
                "url": "https://abc.net.au/ep/301",
                "audio_url": "https://audio2.mp3",
            }
        ]
        mock_detail.return_value = {
            "url": "https://abc.net.au/ep/301",
            "has_transcript": False,
            "episode_id": "301",
            "title": "No Trans Ep",
            "_html": "",
        }

        episodes = collect_all(SETTINGS)

        assert len(episodes) == 1
        assert episodes[0].has_transcript is False
        assert episodes[0].official_transcript == ""
        mock_parse.assert_not_called()
        mock_save.assert_not_called()
        mock_download.assert_not_called()

    @patch("src.collector.time.sleep")
    @patch("src.collector.fetch_episode_detail")
    @patch("src.collector.fetch_episode_list")
    def test_detail_fetch_failure_fallback(self, mock_list, mock_detail, mock_sleep):
        """If detail fetch fails, episode should still appear with has_transcript=False."""
        mock_list.return_value = [
            {
                "episode_id": "302",
                "title": "Fail Ep",
                "description": "",
                "published_date": "2024-07-01",
                "duration_seconds": 500,
                "url": "https://abc.net.au/ep/302",
                "audio_url": "",
            }
        ]
        mock_detail.side_effect = requests.ConnectionError("offline")

        episodes = collect_all(SETTINGS)

        assert len(episodes) == 1
        assert episodes[0].has_transcript is False

    @patch("src.collector.time.sleep")
    @patch("src.collector.fetch_episode_list")
    def test_skip_episode_with_no_url(self, mock_list, mock_sleep):
        mock_list.return_value = [
            {
                "episode_id": "303",
                "title": "No URL",
                "url": "",
            }
        ]
        episodes = collect_all(SETTINGS)
        assert len(episodes) == 0

    @patch("src.collector.time.sleep")
    @patch("src.collector.fetch_episode_list")
    def test_empty_episode_list(self, mock_list, mock_sleep):
        mock_list.return_value = []
        episodes = collect_all(SETTINGS)
        assert episodes == []
