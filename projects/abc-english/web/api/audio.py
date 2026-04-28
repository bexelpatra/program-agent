"""/api/audio/{episode_id} — MP3 streaming with HTTP Range support."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterator, Optional, Tuple

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from ..deps import resolve_project_path

router = APIRouter(prefix="/api/audio", tags=["audio"])

CHUNK_SIZE = 64 * 1024  # 64 KiB

# Allow numeric ids or alphanumeric+hyphen/underscore (no dots, no slashes).
_EPISODE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")

_RANGE_RE = re.compile(r"^\s*bytes=(\d*)-(\d*)\s*$", re.IGNORECASE)


def _validate_episode_id(episode_id: str) -> None:
    if not _EPISODE_ID_RE.match(episode_id or ""):
        raise HTTPException(status_code=400, detail="invalid episode_id")


def _resolve_audio_path(episode_id: str) -> Path:
    path = resolve_project_path(f"data/audio/{episode_id}.mp3")
    # Final defensive check: ensure the resolved path stays inside data/audio.
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


def _parse_range(header: str, file_size: int) -> Optional[Tuple[int, int]]:
    """Parse a ``Range: bytes=start-end`` header.

    Returns ``None`` for unsatisfiable / malformed ranges; caller then
    serves the full file.
    """
    m = _RANGE_RE.match(header)
    if not m:
        return None
    start_s, end_s = m.group(1), m.group(2)
    if start_s == "" and end_s == "":
        return None

    if start_s == "":
        # Suffix range: last N bytes.
        try:
            length = int(end_s)
        except ValueError:
            return None
        if length <= 0:
            return None
        start = max(0, file_size - length)
        end = file_size - 1
    else:
        try:
            start = int(start_s)
        except ValueError:
            return None
        if end_s == "":
            end = file_size - 1
        else:
            try:
                end = int(end_s)
            except ValueError:
                return None

    if start < 0 or start >= file_size or end < start:
        return None
    if end >= file_size:
        end = file_size - 1
    return start, end


def _iter_file(path: Path, start: int, length: int) -> Iterator[bytes]:
    remaining = length
    with open(path, "rb") as fh:
        fh.seek(start)
        while remaining > 0:
            chunk = fh.read(min(CHUNK_SIZE, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk


@router.get("/{episode_id}")
async def stream_audio(episode_id: str, request: Request) -> StreamingResponse:
    _validate_episode_id(episode_id)
    path = _resolve_audio_path(episode_id)
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="audio not found")

    file_size = os.path.getsize(path)
    range_header = request.headers.get("range") or request.headers.get("Range")

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "audio/mpeg",
    }

    if range_header:
        parsed = _parse_range(range_header, file_size)
        if parsed is None:
            # Unsatisfiable range → 416.
            return StreamingResponse(
                iter([b""]),
                status_code=416,
                headers={
                    "Content-Range": f"bytes */{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Type": "audio/mpeg",
                },
            )
        start, end = parsed
        length = end - start + 1
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        headers["Content-Length"] = str(length)
        return StreamingResponse(
            _iter_file(path, start, length),
            status_code=206,
            headers=headers,
            media_type="audio/mpeg",
        )

    headers["Content-Length"] = str(file_size)
    return StreamingResponse(
        _iter_file(path, 0, file_size),
        status_code=200,
        headers=headers,
        media_type="audio/mpeg",
    )
