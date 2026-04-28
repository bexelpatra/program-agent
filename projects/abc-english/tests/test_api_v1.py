"""Integration unit tests for the ``/api/v1/`` namespace (TASK-108).

Covers:

* Bearer authentication contract (parametrized across every v1 endpoint).
* Endpoint happy-path + primary error paths (``/api/v1/episodes``, detail,
  audio, manifest, lookup, notebook CRUD, notebook sync).
* ``create_app()`` fail-fast when ``ABC_API_TOKEN`` is missing.
* Regression: v0 endpoints remain unauthenticated.

Elasticsearch is fully mocked via a dependency override on ``get_es``; the
notebook store is also swapped for an in-memory fake so sync LWW logic can be
exercised deterministically. No real ES connection is made.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from unittest.mock import MagicMock, patch

import pytest

# Make sure the abc-english project root is on sys.path so ``src`` / ``web``
# imports resolve when pytest collects the file from the repo root.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi.testclient import TestClient

TEST_TOKEN = "test-token-123"
WRONG_TOKEN = "nope-nope"

# All authenticated v1 routes. ``payload`` is sent for POST, otherwise None.
# These are the routes whose Bearer-auth behaviour we parametrize over.
V1_AUTHED_ROUTES: List[Tuple[str, str, Optional[Dict[str, Any]]]] = [
    ("GET", "/api/v1/episodes", None),
    ("GET", "/api/v1/episodes/ep-1", None),
    ("GET", "/api/v1/episodes/ep-1/audio", None),
    ("GET", "/api/v1/episodes/ep-1/manifest", None),
    ("GET", "/api/v1/lookup?word=hello", None),
    ("GET", "/api/v1/notebook", None),
    ("POST", "/api/v1/notebook", {"word": "hello"}),
    ("POST", "/api/v1/notebook/sync", {"changes": []}),
]


# ---------------------------------------------------------------------------
# In-memory fakes
# ---------------------------------------------------------------------------


class FakeES:
    """Minimal ES stub that supports the handful of calls v1 endpoints make.

    Seeded via :meth:`seed_episode` / :meth:`seed_sentence`. Unknown indices
    raise the ES ``NotFoundError`` so the handler's except-branch is exercised.
    """

    def __init__(self) -> None:
        # index -> id -> _source
        self.docs: Dict[str, Dict[str, Dict[str, Any]]] = {}

    # --- helpers ----------------------------------------------------------
    def seed_episode(self, index: str, doc: Dict[str, Any]) -> None:
        self.docs.setdefault(index, {})[doc["episode_id"]] = doc

    def seed_sentence(self, index: str, doc: Dict[str, Any]) -> None:
        sid = f"{doc['episode_id']}_{doc['sentence_index']}"
        self.docs.setdefault(index, {})[sid] = doc

    # --- ES-like API ------------------------------------------------------
    def exists(self, *, index: str, id: str) -> bool:
        return id in self.docs.get(index, {})

    def get(self, *, index: str, id: str) -> Dict[str, Any]:
        return {"_source": self.docs[index][id]}

    def search(self, *, index: str, body: Dict[str, Any]) -> Dict[str, Any]:
        store = self.docs.get(index, {})
        query = body.get("query", {})
        sort = body.get("sort") or []
        size = body.get("size", 10)
        frm = body.get("from", 0)

        # Extract simple ``term`` filter (episode_id) from query envelopes.
        def _matches(src: Dict[str, Any]) -> bool:
            if "term" in query:
                for field, val in query["term"].items():
                    if src.get(field) != val:
                        return False
                return True
            if "bool" in query:
                for f in query["bool"].get("filter", []):
                    if "range" in f:
                        for field, cond in f["range"].items():
                            gte = cond.get("gte")
                            if gte is not None and (src.get(field) or "") < gte:
                                return False
                return True
            # match_all
            return True

        hits = [src for src in store.values() if _matches(src)]

        # Sort support: take the first sort key ({field: {order: ...}}).
        if sort:
            key_dict = sort[0]
            field, spec = next(iter(key_dict.items()))
            order = spec.get("order") if isinstance(spec, dict) else "asc"
            reverse = order == "desc"

            def _sort_key(d: Dict[str, Any]) -> Tuple[int, Any]:
                # Sentinel tuple so missing values sort *last* without mixing
                # str/int types (which would raise TypeError in Py3).
                v = d.get(field)
                if v is None:
                    return (1, 0)
                return (0, v)

            hits.sort(key=_sort_key, reverse=reverse)

        total = len(hits)
        paginated = hits[frm : frm + size]
        return {
            "hits": {
                "total": {"value": total},
                "hits": [{"_source": src} for src in paginated],
            }
        }


class FakeNotebookStore:
    """Deterministic replacement for ``src.notebook_v1_store`` calls."""

    def __init__(self) -> None:
        self.by_id: Dict[str, Dict[str, Any]] = {}
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"entry-{self._counter:04d}"

    # Matches src.notebook_v1_store.create_entry signature used by handler.
    def create_entry(
        self,
        payload: Dict[str, Any],
        es: Any = None,
        settings: Any = None,
    ) -> Dict[str, Any]:
        entry_id = self._next_id()
        now = f"2026-04-22T10:00:{self._counter:02d}Z"
        doc: Dict[str, Any] = {
            "id": entry_id,
            "word": payload.get("word") or "",
            "context": payload.get("context") or "",
            "episode_id": payload.get("episode_id") or "",
            "sentence_index": payload.get("sentence_index"),
            "meaning": payload.get("meaning") or "",
            "note": payload.get("note") or "",
            "created_at": now,
            "last_modified": now,
        }
        self.by_id[entry_id] = doc
        return copy.deepcopy(doc)

    def list_entries(
        self,
        since_modified: Optional[str] = None,
        page: int = 1,
        size: int = 20,
        es: Any = None,
        settings: Any = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        items = list(self.by_id.values())
        if since_modified:
            items = [
                d for d in items if (d.get("last_modified") or "") >= since_modified
            ]
        items.sort(key=lambda d: d.get("last_modified") or "", reverse=True)
        total = len(items)
        frm = max(0, (page - 1) * size)
        return copy.deepcopy(items[frm : frm + size]), total

    def patch_entry(
        self,
        entry_id: str,
        payload: Dict[str, Any],
        es: Any = None,
        settings: Any = None,
    ) -> Optional[Dict[str, Any]]:
        existing = self.by_id.get(entry_id)
        if existing is None:
            return None
        updated = dict(existing)
        updated.update(payload)
        self._counter += 1
        updated["last_modified"] = f"2026-04-22T11:00:{self._counter:02d}Z"
        self.by_id[entry_id] = updated
        return copy.deepcopy(updated)

    def delete_entry(
        self,
        entry_id: str,
        es: Any = None,
        settings: Any = None,
    ) -> bool:
        return self.by_id.pop(entry_id, None) is not None

    def upsert_with_id(
        self,
        entry_id: str,
        payload: Dict[str, Any],
        client_last_modified: str,
        es: Any = None,
        settings: Any = None,
    ) -> Tuple[str, Dict[str, Any]]:
        existing = self.by_id.get(entry_id)
        if existing is None:
            now = client_last_modified or "2026-04-22T12:00:00Z"
            doc = {
                "id": entry_id,
                "word": payload.get("word") or "",
                "context": payload.get("context") or "",
                "episode_id": payload.get("episode_id") or "",
                "sentence_index": payload.get("sentence_index"),
                "meaning": payload.get("meaning") or "",
                "note": payload.get("note") or "",
                "created_at": now,
                "last_modified": now,
            }
            self.by_id[entry_id] = doc
            return "applied", copy.deepcopy(doc)

        server_mtime = str(existing.get("last_modified") or "")
        if client_last_modified and client_last_modified > server_mtime:
            doc = dict(existing)
            doc.update(payload)
            doc["last_modified"] = client_last_modified
            self.by_id[entry_id] = doc
            return "applied", copy.deepcopy(doc)
        return "server_wins", copy.deepcopy(existing)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_es() -> FakeES:
    es = FakeES()
    # Seed a couple of episodes + sentences used by the happy-path tests.
    ep_index = "abc-episodes"
    sent_index = "abc-sentences"
    es.seed_episode(
        ep_index,
        {
            "episode_id": "ep-1",
            "title": "Episode 1",
            "published_date": "2026-04-01",
            "duration_seconds": 600,
            "avg_wer": 0.12,
            "has_transcript": True,
            "sentence_count": 3,
            "word_count": 42,
            "url": "https://example.com/ep-1",
            "audio_url": "https://example.com/ep-1.mp3",
        },
    )
    es.seed_episode(
        ep_index,
        {
            "episode_id": "ep-2",
            "title": "Episode 2",
            "published_date": "2026-04-10",
            "duration_seconds": 720,
            "avg_wer": 0.08,
            "has_transcript": True,
            "sentence_count": 5,
            "word_count": 70,
        },
    )
    # Seed sentences out-of-order so the asc-sort assertion is meaningful.
    for i in (2, 0, 1):
        es.seed_sentence(
            sent_index,
            {
                "episode_id": "ep-1",
                "sentence_index": i,
                "official_text": f"Sentence {i}.",
                "start_time": i * 1.0,
                "end_time": (i + 1) * 1.0,
                "wer": 0.1 + i * 0.05,
                "difficulty": "B1",
            },
        )
    return es


@pytest.fixture
def fake_notebook() -> FakeNotebookStore:
    return FakeNotebookStore()


@pytest.fixture
def app_client(monkeypatch, fake_es, fake_notebook):
    """Build the FastAPI app with ES + notebook_v1_store patched out."""
    monkeypatch.setenv("ABC_API_TOKEN", TEST_TOKEN)

    # Patch es_client.get_client so create_app() / get_es never hits a real ES.
    # Note: load_settings() still reads settings.yaml but that's fine.
    import src.es_client as es_client_mod

    def _fake_get_client(config_path=None, settings=None):
        return fake_es

    monkeypatch.setattr(es_client_mod, "get_client", _fake_get_client)

    # Patch ollama model verification so startup hook stays silent.
    import src.ollama_client as ollama_mod

    async def _noop_verify(settings):
        return {"ok": True}

    monkeypatch.setattr(ollama_mod, "verify_ollama_model", _noop_verify)

    # Patch notebook_v1_store functions that the route handlers call through.
    import src.notebook_v1_store as store_mod

    monkeypatch.setattr(store_mod, "create_entry", fake_notebook.create_entry)
    monkeypatch.setattr(store_mod, "list_entries", fake_notebook.list_entries)
    monkeypatch.setattr(store_mod, "patch_entry", fake_notebook.patch_entry)
    monkeypatch.setattr(store_mod, "delete_entry", fake_notebook.delete_entry)
    monkeypatch.setattr(store_mod, "upsert_with_id", fake_notebook.upsert_with_id)

    # The notebook router imports the module aliases at import time, so patch
    # those references too.
    import web.api.v1.notebook as notebook_router_mod

    monkeypatch.setattr(
        notebook_router_mod.notebook_v1_store,
        "create_entry",
        fake_notebook.create_entry,
    )
    monkeypatch.setattr(
        notebook_router_mod.notebook_v1_store,
        "list_entries",
        fake_notebook.list_entries,
    )
    monkeypatch.setattr(
        notebook_router_mod.notebook_v1_store, "patch_entry", fake_notebook.patch_entry
    )
    monkeypatch.setattr(
        notebook_router_mod.notebook_v1_store,
        "delete_entry",
        fake_notebook.delete_entry,
    )
    monkeypatch.setattr(
        notebook_router_mod.notebook_v1_store,
        "upsert_with_id",
        fake_notebook.upsert_with_id,
    )

    from web.app import create_app

    app = create_app()
    with TestClient(app) as client:
        yield client


def _auth_headers(token: str = TEST_TOKEN) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


# ===========================================================================
# Bearer authentication contract
# ===========================================================================


class TestBearerAuth:
    """Every v1 authenticated route returns 401 unless a valid Bearer is given."""

    @pytest.mark.parametrize("method,path,payload", V1_AUTHED_ROUTES)
    def test_missing_header_returns_401(self, app_client, method, path, payload):
        response = app_client.request(method, path, json=payload)
        assert (
            response.status_code == 401
        ), f"{method} {path} without Authorization should be 401, got {response.status_code}"

    @pytest.mark.parametrize("method,path,payload", V1_AUTHED_ROUTES)
    def test_non_bearer_scheme_returns_401(self, app_client, method, path, payload):
        response = app_client.request(
            method, path, json=payload, headers={"Authorization": "NotBearer xxx"}
        )
        assert response.status_code == 401

    @pytest.mark.parametrize("method,path,payload", V1_AUTHED_ROUTES)
    def test_wrong_token_returns_401(self, app_client, method, path, payload):
        response = app_client.request(
            method, path, json=payload, headers=_auth_headers(WRONG_TOKEN)
        )
        assert response.status_code == 401

    @pytest.mark.parametrize("method,path,payload", V1_AUTHED_ROUTES)
    def test_bearer_with_empty_token_returns_401(
        self, app_client, method, path, payload
    ):
        response = app_client.request(
            method, path, json=payload, headers={"Authorization": "Bearer "}
        )
        assert response.status_code == 401

    @pytest.mark.parametrize("method,path,payload", V1_AUTHED_ROUTES)
    def test_correct_bearer_is_not_401(self, app_client, method, path, payload):
        """Correct token must not produce 401. (Actual code may be 200/404/422.)"""
        response = app_client.request(
            method, path, json=payload, headers=_auth_headers()
        )
        assert response.status_code != 401, (
            f"{method} {path} with correct token should not be 401, "
            f"got {response.status_code}: {response.text}"
        )


# ===========================================================================
# GET /api/v1/episodes
# ===========================================================================


class TestListEpisodes:
    def test_happy_path_envelope(self, app_client):
        response = app_client.get("/api/v1/episodes", headers=_auth_headers())
        assert response.status_code == 200
        body = response.json()
        assert set(body.keys()) == {"episodes", "total", "page", "size"}
        assert isinstance(body["episodes"], list)
        assert body["total"] == 2
        assert body["page"] == 1
        assert body["size"] == 20
        # published_date desc: ep-2 (2026-04-10) before ep-1 (2026-04-01)
        ids = [e["id"] for e in body["episodes"]]
        assert ids == ["ep-2", "ep-1"]
        # v1 synthetic fields present
        for ep in body["episodes"]:
            assert "id" in ep
            assert "last_modified" in ep
            assert "duration" in ep

    def test_page_lower_bound_rejected(self, app_client):
        response = app_client.get("/api/v1/episodes?page=0", headers=_auth_headers())
        assert response.status_code == 422

    def test_page_negative_rejected(self, app_client):
        response = app_client.get("/api/v1/episodes?page=-1", headers=_auth_headers())
        assert response.status_code == 422

    def test_size_zero_rejected(self, app_client):
        response = app_client.get("/api/v1/episodes?size=0", headers=_auth_headers())
        assert response.status_code == 422

    def test_size_above_50_rejected(self, app_client):
        response = app_client.get("/api/v1/episodes?size=51", headers=_auth_headers())
        assert response.status_code == 422

    def test_since_modified_invalid_returns_422(self, app_client):
        """Malformed ISO8601 must trigger FastAPI's 422 via Query regex."""
        response = app_client.get(
            "/api/v1/episodes?since_modified=not-a-date",
            headers=_auth_headers(),
        )
        assert (
            response.status_code == 422
        ), f"malformed since_modified should be 422, got {response.status_code}"


# ===========================================================================
# GET /api/v1/episodes/{id}
# ===========================================================================


class TestEpisodeDetail:
    def test_happy_path_shape(self, app_client):
        response = app_client.get("/api/v1/episodes/ep-1", headers=_auth_headers())
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == "ep-1"
        assert body["title"] == "Episode 1"
        assert "sentences" in body
        assert isinstance(body["sentences"], list)
        assert len(body["sentences"]) == 3
        # Must be sorted ascending by index even though FakeES seeded out-of-order.
        indexes = [s["index"] for s in body["sentences"]]
        assert indexes == [0, 1, 2]
        # ms timestamps computed from seconds
        assert body["sentences"][0]["start_ms"] == 0
        assert body["sentences"][1]["start_ms"] == 1000

    def test_missing_episode_returns_404(self, app_client):
        response = app_client.get(
            "/api/v1/episodes/does-not-exist", headers=_auth_headers()
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "episode not found"}


# ===========================================================================
# GET /api/v1/episodes/{id}/audio
# ===========================================================================


class TestAudio:
    def test_missing_file_returns_404(self, app_client):
        # No MP3 exists under data/audio in the test env -> v0 handler raises 404.
        response = app_client.get(
            "/api/v1/episodes/ep-1/audio", headers=_auth_headers()
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "audio not found"

    def test_happy_path_serves_bytes(self, app_client, tmp_path, monkeypatch):
        """If a file is present, v1 should stream it (delegates to v0)."""
        # Point resolve_project_path to a tmp dir containing the file.
        import web.deps as web_deps_mod
        import web.api.audio as audio_v0
        import web.api.v1.manifest as manifest_mod

        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True)
        (audio_dir / "ep-1.mp3").write_bytes(b"\xff\xfb\x90\x00hello-mp3-bytes")

        def _fake_resolve(rel: str) -> Path:
            return tmp_path / rel

        monkeypatch.setattr(web_deps_mod, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(audio_v0, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(manifest_mod, "resolve_project_path", _fake_resolve)

        response = app_client.get(
            "/api/v1/episodes/ep-1/audio", headers=_auth_headers()
        )
        assert response.status_code == 200
        assert response.content == b"\xff\xfb\x90\x00hello-mp3-bytes"
        assert response.headers.get("content-type", "").startswith("audio/mpeg")
        assert response.headers.get("accept-ranges") == "bytes"

    def test_range_header_returns_206(self, app_client, tmp_path, monkeypatch):
        import web.deps as web_deps_mod
        import web.api.audio as audio_v0
        import web.api.v1.manifest as manifest_mod

        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True)
        (audio_dir / "ep-1.mp3").write_bytes(b"0123456789")

        def _fake_resolve(rel: str) -> Path:
            return tmp_path / rel

        monkeypatch.setattr(web_deps_mod, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(audio_v0, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(manifest_mod, "resolve_project_path", _fake_resolve)

        response = app_client.get(
            "/api/v1/episodes/ep-1/audio",
            headers={**_auth_headers(), "Range": "bytes=2-5"},
        )
        assert response.status_code == 206
        assert response.content == b"2345"
        assert response.headers.get("content-range") == "bytes 2-5/10"


# ===========================================================================
# GET /api/v1/episodes/{id}/manifest
# ===========================================================================


class TestManifest:
    def test_missing_file_returns_empty_files(self, app_client):
        response = app_client.get(
            "/api/v1/episodes/ep-1/manifest", headers=_auth_headers()
        )
        assert response.status_code == 200
        body = response.json()
        assert body["episode_id"] == "ep-1"
        assert body["files"] == []

    def test_present_file_exposes_sha256(self, app_client, tmp_path, monkeypatch):
        import web.deps as web_deps_mod
        import web.api.audio as audio_v0
        import web.api.v1.manifest as manifest_mod

        audio_dir = tmp_path / "data" / "audio"
        audio_dir.mkdir(parents=True)
        (audio_dir / "ep-1.mp3").write_bytes(b"abc")

        def _fake_resolve(rel: str) -> Path:
            return tmp_path / rel

        monkeypatch.setattr(web_deps_mod, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(audio_v0, "resolve_project_path", _fake_resolve)
        monkeypatch.setattr(manifest_mod, "resolve_project_path", _fake_resolve)

        response = app_client.get(
            "/api/v1/episodes/ep-1/manifest", headers=_auth_headers()
        )
        assert response.status_code == 200
        body = response.json()
        assert body["episode_id"] == "ep-1"
        assert len(body["files"]) == 1
        f = body["files"][0]
        assert f["kind"] == "audio"
        assert f["url"] == "/api/v1/episodes/ep-1/audio"
        assert f["size_bytes"] == 3
        # sha256("abc") precomputed.
        assert f["sha256"] == (
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        )


# ===========================================================================
# GET /api/v1/lookup
# ===========================================================================


class TestLookup:
    def test_missing_word_returns_422(self, app_client):
        response = app_client.get("/api/v1/lookup", headers=_auth_headers())
        assert response.status_code == 422

    def test_empty_word_returns_422(self, app_client):
        response = app_client.get("/api/v1/lookup?word=", headers=_auth_headers())
        assert response.status_code == 422

    def test_happy_path_returns_source_field(self, app_client, monkeypatch):
        """v1 delegates to v0 post_lookup. Patch the LLM path to a stub."""
        # Patch llm_cache.get_cached to return a canned entry so no ollama call.
        import src.llm_cache as llm_cache_mod

        monkeypatch.setattr(
            llm_cache_mod,
            "get_cached",
            lambda term, model, prompt_version, es=None: {
                "term": term,
                "term_type": "word",
                "explanation_en": "a greeting",
                "examples": ["Hello, world!"],
            },
        )

        response = app_client.get("/api/v1/lookup?word=hello", headers=_auth_headers())
        assert response.status_code == 200
        body = response.json()
        assert body.get("source") == "cache"
        assert body["term"] == "hello"
        assert body["term_type"] == "word"


# ===========================================================================
# Notebook CRUD (/api/v1/notebook)
# ===========================================================================


class TestNotebookCRUD:
    def test_create_returns_201_with_id_and_timestamps(self, app_client):
        response = app_client.post(
            "/api/v1/notebook",
            json={"word": "hello", "meaning": "a greeting"},
            headers=_auth_headers(),
        )
        assert response.status_code == 201
        body = response.json()
        assert body["word"] == "hello"
        assert body["meaning"] == "a greeting"
        assert body["id"]
        assert body["created_at"]
        assert body["last_modified"]
        # created_at == last_modified on first write
        assert body["created_at"] == body["last_modified"]

    def test_list_includes_created_entry(self, app_client):
        create = app_client.post(
            "/api/v1/notebook",
            json={"word": "world"},
            headers=_auth_headers(),
        )
        assert create.status_code == 201
        entry_id = create.json()["id"]

        response = app_client.get("/api/v1/notebook", headers=_auth_headers())
        assert response.status_code == 200
        body = response.json()
        assert set(body.keys()) == {"entries", "total", "page", "size"}
        assert body["total"] >= 1
        assert any(e["id"] == entry_id for e in body["entries"])

    def test_patch_updates_fields_and_bumps_last_modified(self, app_client):
        create = app_client.post(
            "/api/v1/notebook",
            json={"word": "flux"},
            headers=_auth_headers(),
        )
        entry_id = create.json()["id"]
        original_lm = create.json()["last_modified"]

        response = app_client.patch(
            f"/api/v1/notebook/{entry_id}",
            json={"meaning": "continuous change"},
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        body = response.json()
        assert body["meaning"] == "continuous change"
        # last_modified must be strictly greater.
        assert body["last_modified"] > original_lm

    def test_patch_missing_entry_returns_404(self, app_client):
        response = app_client.patch(
            "/api/v1/notebook/no-such-id",
            json={"meaning": "x"},
            headers=_auth_headers(),
        )
        assert response.status_code == 404

    def test_delete_returns_204_and_entry_gone(self, app_client):
        create = app_client.post(
            "/api/v1/notebook",
            json={"word": "gone"},
            headers=_auth_headers(),
        )
        entry_id = create.json()["id"]

        response = app_client.delete(
            f"/api/v1/notebook/{entry_id}", headers=_auth_headers()
        )
        assert response.status_code == 204

        listing = app_client.get("/api/v1/notebook", headers=_auth_headers()).json()
        assert not any(e["id"] == entry_id for e in listing["entries"])

    def test_delete_missing_entry_returns_404(self, app_client):
        response = app_client.delete(
            "/api/v1/notebook/no-such-id", headers=_auth_headers()
        )
        assert response.status_code == 404


# ===========================================================================
# Notebook /sync (LWW semantics)
# ===========================================================================


class TestNotebookSync:
    def test_upsert_new_id_client_wins(self, app_client):
        """Upsert with a fresh id and client_last_modified → 'applied'."""
        response = app_client.post(
            "/api/v1/notebook/sync",
            json={
                "changes": [
                    {
                        "id": "manual-uuid-a",
                        "op": "upsert",
                        "payload": {"word": "alpha", "meaning": "first letter"},
                        "client_last_modified": "2026-05-01T10:00:00Z",
                    }
                ]
            },
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        results = response.json()["results"]
        assert len(results) == 1
        r = results[0]
        assert r["id"] == "manual-uuid-a"
        assert r["status"] == "applied"
        assert r["server_last_modified"] == "2026-05-01T10:00:00Z"

    def test_upsert_server_wins_when_server_newer(self, app_client, fake_notebook):
        """Server copy is newer → status='server_wins', no overwrite."""
        # Seed a server-side doc with a very recent last_modified.
        fake_notebook.by_id["shared-id"] = {
            "id": "shared-id",
            "word": "original",
            "context": "",
            "episode_id": "",
            "sentence_index": None,
            "meaning": "server value",
            "note": "",
            "created_at": "2026-04-22T09:00:00Z",
            "last_modified": "2026-06-01T00:00:00Z",  # newer than client below
        }

        response = app_client.post(
            "/api/v1/notebook/sync",
            json={
                "changes": [
                    {
                        "id": "shared-id",
                        "op": "upsert",
                        "payload": {"meaning": "client value"},
                        "client_last_modified": "2026-05-01T00:00:00Z",
                    }
                ]
            },
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        r = response.json()["results"][0]
        assert r["status"] == "server_wins"
        # Server copy must be unchanged.
        assert fake_notebook.by_id["shared-id"]["meaning"] == "server value"

    def test_upsert_applied_when_client_newer(self, app_client, fake_notebook):
        fake_notebook.by_id["shared-id-2"] = {
            "id": "shared-id-2",
            "word": "w",
            "context": "",
            "episode_id": "",
            "sentence_index": None,
            "meaning": "old",
            "note": "",
            "created_at": "2026-04-22T09:00:00Z",
            "last_modified": "2026-04-22T09:00:00Z",
        }
        response = app_client.post(
            "/api/v1/notebook/sync",
            json={
                "changes": [
                    {
                        "id": "shared-id-2",
                        "op": "upsert",
                        "payload": {"meaning": "new"},
                        "client_last_modified": "2026-05-01T00:00:00Z",
                    }
                ]
            },
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        r = response.json()["results"][0]
        assert r["status"] == "applied"
        assert fake_notebook.by_id["shared-id-2"]["meaning"] == "new"
        assert (
            fake_notebook.by_id["shared-id-2"]["last_modified"]
            == "2026-05-01T00:00:00Z"
        )

    def test_delete_existing_is_applied(self, app_client, fake_notebook):
        fake_notebook.by_id["del-me"] = {
            "id": "del-me",
            "word": "x",
            "last_modified": "2026-04-22T09:00:00Z",
        }
        response = app_client.post(
            "/api/v1/notebook/sync",
            json={"changes": [{"id": "del-me", "op": "delete"}]},
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        r = response.json()["results"][0]
        assert r["status"] == "applied"
        assert "del-me" not in fake_notebook.by_id

    def test_delete_missing_returns_not_found(self, app_client):
        response = app_client.post(
            "/api/v1/notebook/sync",
            json={"changes": [{"id": "ghost", "op": "delete"}]},
            headers=_auth_headers(),
        )
        assert response.status_code == 200
        r = response.json()["results"][0]
        assert r["status"] == "not_found"


# ===========================================================================
# create_app() token configuration
# ===========================================================================


class TestCreateAppTokenConfig:
    def test_missing_token_raises_runtime_error(self, monkeypatch):
        """No ABC_API_TOKEN + empty settings.api_token → RuntimeError."""
        monkeypatch.delenv("ABC_API_TOKEN", raising=False)

        # Load settings then force api_token empty.
        import src.es_client as es_client_mod

        orig_load = es_client_mod.load_settings

        def _empty_token_load(config_path=None):
            s = orig_load(config_path)
            s["api_token"] = ""
            return s

        monkeypatch.setattr(es_client_mod, "load_settings", _empty_token_load)
        # Stop ES + ollama side-effects.
        monkeypatch.setattr(
            es_client_mod,
            "get_client",
            lambda config_path=None, settings=None: MagicMock(),
        )
        import src.ollama_client as ollama_mod

        async def _noop_verify(settings):
            return {"ok": True}

        monkeypatch.setattr(ollama_mod, "verify_ollama_model", _noop_verify)

        from web.app import create_app

        with pytest.raises(RuntimeError) as excinfo:
            create_app()
        assert "api_token" in str(excinfo.value)

    def test_env_token_overrides_empty_yaml(self, monkeypatch):
        """Env var is sufficient even when settings.api_token is empty."""
        monkeypatch.setenv("ABC_API_TOKEN", "from-env")

        import src.es_client as es_client_mod

        orig_load = es_client_mod.load_settings

        def _empty_token_load(config_path=None):
            s = orig_load(config_path)
            s["api_token"] = ""
            return s

        monkeypatch.setattr(es_client_mod, "load_settings", _empty_token_load)
        monkeypatch.setattr(
            es_client_mod,
            "get_client",
            lambda config_path=None, settings=None: MagicMock(),
        )
        import src.ollama_client as ollama_mod

        async def _noop_verify(settings):
            return {"ok": True}

        monkeypatch.setattr(ollama_mod, "verify_ollama_model", _noop_verify)

        from web.app import create_app

        app = create_app()
        # Basic smoke: the v1 router must be mounted.
        paths = {r.path for r in app.router.routes if hasattr(r, "path")}
        assert any(p.startswith("/api/v1/") for p in paths)


# ===========================================================================
# Regression: v0 endpoints remain unauthenticated
# ===========================================================================


class TestV0Regression:
    def test_health_without_bearer(self, app_client):
        response = app_client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_v0_episodes_without_bearer(self, app_client):
        """/api/episodes is the v0 listing — must not require a Bearer."""
        response = app_client.get("/api/episodes")
        # With FakeES seeded, this returns 200. Either way, not 401.
        assert response.status_code != 401
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 2
