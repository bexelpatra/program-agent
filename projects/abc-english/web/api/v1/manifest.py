"""/api/v1/episodes/{id}/manifest — downloadable-file manifest for the app.

Returns a small JSON envelope describing the audio file (URL, size, sha256).
The response is always 200 — a missing audio file yields an empty ``files``
array (per task spec), not 404. The mobile client can then decide whether to
re-sync or show a placeholder.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Request

from ...deps import resolve_project_path
from .. import audio as audio_v0

router = APIRouter(prefix="/episodes", tags=["v1", "manifest"])


def _sha256_of_file(path: Path, chunk_size: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_audio_path(episode_id: str) -> Path:
    """Path-traversal safe audio path lookup. Re-uses v0 validation rules."""
    audio_v0._validate_episode_id(episode_id)
    path = resolve_project_path(f"data/audio/{episode_id}.mp3")
    audio_root = resolve_project_path("data/audio").resolve()
    try:
        resolved = path.resolve()
    except FileNotFoundError:
        resolved = path
    try:
        resolved.relative_to(audio_root)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid episode_id")
    return path


@router.get("/{episode_id}/manifest")
async def get_manifest(episode_id: str, request: Request) -> Dict[str, Any]:
    path = _resolve_audio_path(episode_id)

    files: List[Dict[str, Any]] = []
    if path.exists() and path.is_file():
        size_bytes = os.path.getsize(path)
        files.append(
            {
                "kind": "audio",
                "url": f"/api/v1/episodes/{episode_id}/audio",
                "size_bytes": size_bytes,
                "sha256": _sha256_of_file(path),
            }
        )
    return {"episode_id": episode_id, "files": files}
