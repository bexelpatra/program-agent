"""Whisper-based audio transcription module.

Transcribes MP3 audio files using OpenAI Whisper, extracting text with
per-segment timestamps.  Results are saved as JSON files alongside
the official transcripts produced by the collector.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import whisper

from .es_client import load_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton model cache
# ---------------------------------------------------------------------------

_model: Optional[whisper.Whisper] = None
_model_name: Optional[str] = None


def load_model(settings: dict) -> whisper.Whisper:
    """Load (or return cached) Whisper model based on settings.

    The model is cached as a module-level singleton.  If the requested
    model name differs from the currently loaded one the old model is
    discarded and the new one is loaded.

    Args:
        settings: Full settings dict (must contain a ``whisper`` section).

    Returns:
        A loaded ``whisper.Whisper`` model instance.
    """
    global _model, _model_name

    whisper_cfg = settings.get("whisper", {})
    name = whisper_cfg.get("model", "base")
    device = whisper_cfg.get("device", "cpu")

    if _model is not None and _model_name == name:
        return _model

    logger.info("Loading Whisper model '%s' on device '%s'...", name, device)
    _model = whisper.load_model(name, device=device)
    _model_name = name
    logger.info("Whisper model '%s' loaded.", name)
    return _model


# ---------------------------------------------------------------------------
# Core transcription
# ---------------------------------------------------------------------------


def transcribe_audio(audio_path: str, model: whisper.Whisper) -> dict:
    """Transcribe a single audio file and return structured results.

    Args:
        audio_path: Path to the MP3 (or other audio) file.
        model: A loaded Whisper model.

    Returns:
        A dict with keys:
        - ``full_text``: The complete transcription string.
        - ``segments``: A list of dicts, each with ``text``, ``start``,
          and ``end`` (seconds as floats).
    """
    logger.info("Transcribing: %s", audio_path)
    result = model.transcribe(str(audio_path), language="en")

    segments = [
        {
            "text": seg["text"].strip(),
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
        }
        for seg in result.get("segments", [])
        if seg.get("text", "").strip()
    ]

    full_text = result.get("text", "").strip()
    return {"full_text": full_text, "segments": segments}


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def _resolve_transcript_dir(settings: dict) -> Path:
    """Resolve the transcript output directory from settings."""
    data_conf = settings.get("data", {})
    transcript_dir = data_conf.get("transcript_dir", "data/transcripts")
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / transcript_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _resolve_audio_dir(settings: dict) -> Path:
    """Resolve the audio directory from settings."""
    data_conf = settings.get("data", {})
    audio_dir = data_conf.get("audio_dir", "data/audio")
    project_root = Path(__file__).resolve().parent.parent
    return project_root / audio_dir


def save_whisper_transcript(
    episode_id: str,
    result: dict,
    settings: dict,
) -> str:
    """Save Whisper transcription result as a JSON file.

    The file is written to ``{data.transcript_dir}/{episode_id}_whisper.json``.

    Args:
        episode_id: Unique episode identifier.
        result: Dict from :func:`transcribe_audio` (must have ``full_text``
                and ``segments`` keys).
        settings: Loaded settings dict.

    Returns:
        Absolute path to the saved JSON file.
    """
    out_dir = _resolve_transcript_dir(settings)
    out_path = out_dir / f"{episode_id}_whisper.json"

    payload = {
        "episode_id": episode_id,
        "segments": result.get("segments", []),
        "full_text": result.get("full_text", ""),
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    logger.info("Saved Whisper transcript for %s -> %s", episode_id, out_path)
    return str(out_path)


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------


def _whisper_transcript_exists(episode_id: str, settings: dict) -> bool:
    """Check whether a Whisper transcript JSON already exists."""
    out_dir = _resolve_transcript_dir(settings)
    return (out_dir / f"{episode_id}_whisper.json").exists()


def transcribe_episode(episode_id: str, settings: dict) -> dict:
    """Transcribe a single episode end-to-end.

    Loads the Whisper model (singleton), locates the MP3, transcribes it,
    and saves the result as JSON.

    If a Whisper transcript already exists for this episode the
    transcription is skipped and the existing data is returned.

    Args:
        episode_id: Unique episode identifier.
        settings: Loaded settings dict.

    Returns:
        A dict with keys ``episode_id``, ``segments``, ``full_text``,
        ``path`` (saved file path), and ``skipped`` (bool).
    """
    # Duplicate prevention
    if _whisper_transcript_exists(episode_id, settings):
        logger.info("Whisper transcript already exists for %s, skipping.", episode_id)
        out_dir = _resolve_transcript_dir(settings)
        existing_path = out_dir / f"{episode_id}_whisper.json"
        with open(existing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["path"] = str(existing_path)
        data["skipped"] = True
        return data

    # Locate audio file
    audio_dir = _resolve_audio_dir(settings)
    audio_path = audio_dir / f"{episode_id}.mp3"
    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found for episode {episode_id}: {audio_path}"
        )

    # Transcribe
    model = load_model(settings)
    result = transcribe_audio(str(audio_path), model)

    # Save
    saved_path = save_whisper_transcript(episode_id, result, settings)

    return {
        "episode_id": episode_id,
        "segments": result["segments"],
        "full_text": result["full_text"],
        "path": saved_path,
        "skipped": False,
    }


def transcribe_all(
    episode_ids: List[str],
    settings: Optional[dict] = None,
) -> List[dict]:
    """Batch-transcribe multiple episodes.

    Already-transcribed episodes are automatically skipped.

    Args:
        episode_ids: List of episode identifiers to process.
        settings: Loaded settings dict.  If None, loads from default path.

    Returns:
        A list of result dicts (one per episode), each matching the
        return format of :func:`transcribe_episode`.
    """
    if settings is None:
        settings = load_settings()

    results: List[dict] = []
    total = len(episode_ids)

    for idx, episode_id in enumerate(episode_ids, 1):
        logger.info("Transcribing episode %d/%d: %s", idx, total, episode_id)
        try:
            result = transcribe_episode(episode_id, settings)
            results.append(result)
            status = "skipped" if result.get("skipped") else "done"
            logger.info(
                "Episode %s: %s (%d segments)",
                episode_id,
                status,
                len(result.get("segments", [])),
            )
        except FileNotFoundError as exc:
            logger.warning("Skipping %s: %s", episode_id, exc)
            results.append(
                {
                    "episode_id": episode_id,
                    "segments": [],
                    "full_text": "",
                    "path": "",
                    "skipped": False,
                    "error": str(exc),
                }
            )
        except Exception as exc:
            logger.error("Failed to transcribe %s: %s", episode_id, exc)
            results.append(
                {
                    "episode_id": episode_id,
                    "segments": [],
                    "full_text": "",
                    "path": "",
                    "skipped": False,
                    "error": str(exc),
                }
            )

    done = sum(1 for r in results if r.get("full_text") and not r.get("error"))
    skipped = sum(1 for r in results if r.get("skipped"))
    failed = sum(1 for r in results if r.get("error"))
    logger.info(
        "Batch transcription complete: %d total, %d done, %d skipped, %d failed",
        total,
        done,
        skipped,
        failed,
    )
    return results
