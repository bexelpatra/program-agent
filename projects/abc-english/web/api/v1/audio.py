"""/api/v1/episodes/{id}/audio — MP3 streaming with Range support.

Delegates to the v0 handler in :mod:`web.api.audio` to avoid duplicating
Range-parsing logic. Only the URL shape differs.
"""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .. import audio as audio_v0

router = APIRouter(prefix="/episodes", tags=["v1", "audio"])


@router.get("/{episode_id}/audio")
async def stream_audio_v1(episode_id: str, request: Request) -> StreamingResponse:
    """Thin wrapper over :func:`web.api.audio.stream_audio`."""
    return await audio_v0.stream_audio(episode_id, request)
