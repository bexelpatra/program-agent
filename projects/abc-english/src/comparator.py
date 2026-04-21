"""Comparator module: official vs Whisper transcript comparison.

Computes Word Error Rate (WER) between official and Whisper transcripts,
matches sentences to Whisper segments via greedy alignment, and assigns
listening-difficulty labels based on WER thresholds.
"""

import difflib
import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .es_client import load_settings
from .models import Sentence

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _resolve_transcript_dir(settings: dict) -> Path:
    """Resolve the transcript directory from settings."""
    data_conf = settings.get("data", {})
    transcript_dir = data_conf.get("transcript_dir", "data/transcripts")
    return _PROJECT_ROOT / transcript_dir


# ---------------------------------------------------------------------------
# Text normalisation
# ---------------------------------------------------------------------------


def _normalise(text: str) -> List[str]:
    """Lower-case, strip punctuation, and tokenise into words.

    Returns a list of word tokens suitable for WER comparison.
    """
    text = text.lower()
    # Remove punctuation (keep only letters, digits, whitespace)
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    # Collapse whitespace
    tokens = text.split()
    return tokens


# ---------------------------------------------------------------------------
# WER calculation (Levenshtein distance on word sequences)
# ---------------------------------------------------------------------------


def calculate_wer(reference: str, hypothesis: str) -> float:
    """Compute Word Error Rate between *reference* and *hypothesis*.

    Both strings are normalised (lower-cased, punctuation removed) before
    comparison.  WER is defined as::

        WER = (S + D + I) / N

    where S = substitutions, D = deletions, I = insertions, and
    N = number of words in the reference.

    Returns 0.0 when both strings are empty.  Returns 1.0 when the
    reference is empty but the hypothesis is not.
    """
    ref_tokens = _normalise(reference)
    hyp_tokens = _normalise(hypothesis)

    n = len(ref_tokens)
    m = len(hyp_tokens)

    if n == 0 and m == 0:
        return 0.0
    if n == 0:
        return 1.0

    # Dynamic-programming Levenshtein at the word level.
    # We only need two rows at a time to save memory.
    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        curr[0] = i
        for j in range(1, m + 1):
            cost = 0 if ref_tokens[i - 1] == hyp_tokens[j - 1] else 1
            curr[j] = min(
                prev[j] + 1,  # deletion
                curr[j - 1] + 1,  # insertion
                prev[j - 1] + cost,  # substitution
            )
        prev, curr = curr, prev

    distance = prev[m]
    return distance / n


# ---------------------------------------------------------------------------
# Listening difficulty
# ---------------------------------------------------------------------------


def calculate_listening_difficulty(wer: float) -> str:
    """Classify listening difficulty from a WER value.

    Thresholds:
        * 0.00 -- 0.05  ->  ``"easy"``
        * 0.05 -- 0.15  ->  ``"medium"``
        * 0.15 -- 0.30  ->  ``"hard"``
        * 0.30+         ->  ``"very_hard"``
    """
    if wer <= 0.05:
        return "easy"
    if wer <= 0.15:
        return "medium"
    if wer <= 0.30:
        return "hard"
    return "very_hard"


# ---------------------------------------------------------------------------
# Sentence-level comparison (greedy alignment)
# ---------------------------------------------------------------------------


def compare_sentences(
    official_sentences: List[str],
    whisper_segments: List[dict],
) -> List[dict]:
    """Match official sentences to Whisper segments via word-level alignment.

    Uses :class:`difflib.SequenceMatcher` on normalised token streams to
    find matching blocks between the whisper audio transcript and the
    official sentence-split transcript. Unmatched whisper tokens (intros,
    ads, outros) are naturally skipped because they have no counterpart
    in the official transcript.

    For each official sentence, the matched whisper token indices are
    collected; the timestamps come from the whisper segments covering
    those tokens. Sentences with no match fall back to the previous
    sentence's end time (timestamp interpolation) so the UI never jumps
    to 0:00 mid-stream.
    """
    # Flat whisper tokens: (normalised_token, segment_idx)
    whisper_tokens: List[Tuple[str, int]] = []
    for seg_idx, seg in enumerate(whisper_segments):
        for tok in _normalise(seg.get("text", "")):
            whisper_tokens.append((tok, seg_idx))

    # Flat official tokens grouped per sentence (start, end) range.
    official_tokens: List[str] = []
    sent_ranges: List[Tuple[int, int]] = []
    for sent in official_sentences:
        start = len(official_tokens)
        official_tokens.extend(_normalise(sent))
        sent_ranges.append((start, len(official_tokens)))

    a = [t[0] for t in whisper_tokens]  # whisper token stream
    b = official_tokens  # official token stream

    # Map each official token position -> matched whisper token position.
    official_to_whisper: List[Optional[int]] = [None] * len(b)
    if a and b:
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        for block in sm.get_matching_blocks():
            for k in range(block.size):
                official_to_whisper[block.b + k] = block.a + k

    results: List[dict] = []
    last_end_time = 0.0

    for sent_idx, (tok_start, tok_end) in enumerate(sent_ranges):
        matched = [
            official_to_whisper[i]
            for i in range(tok_start, tok_end)
            if official_to_whisper[i] is not None
        ]

        if matched:
            w_lo, w_hi = min(matched), max(matched)
            # Whisper text = the aligned token span (includes any
            # unmatched whisper tokens sitting inside the span so the
            # user can see what the audio actually says).
            whisper_text = " ".join(a[w_lo : w_hi + 1])
            start_seg = whisper_tokens[w_lo][1]
            end_seg = whisper_tokens[w_hi][1]
            start_time = float(whisper_segments[start_seg]["start"])
            end_time = float(whisper_segments[end_seg]["end"])
            last_end_time = end_time
        else:
            # No alignment — pin to previous sentence's end so the
            # subtitle doesn't snap back to the intro.
            whisper_text = ""
            start_time = last_end_time
            end_time = last_end_time

        official_text = official_sentences[sent_idx]
        wer = (
            calculate_wer(official_text, whisper_text)
            if whisper_text
            else (1.0 if official_text.strip() else 0.0)
        )

        results.append(
            {
                "sentence_index": sent_idx,
                "official_text": official_text,
                "whisper_text": whisper_text,
                "start_time": start_time,
                "end_time": end_time,
                "wer": round(wer, 4),
                "listening_difficulty": calculate_listening_difficulty(wer),
            }
        )

    return results


# ---------------------------------------------------------------------------
# Episode-level comparison
# ---------------------------------------------------------------------------


def compare_episode(
    episode_id: str,
    settings: Optional[dict] = None,
) -> Tuple[List[Sentence], float]:
    """Compare official and Whisper transcripts for a single episode.

    Loads both JSON files, runs :func:`compare_sentences`, and converts
    the results into :class:`~models.Sentence` instances.

    Args:
        episode_id: Unique episode identifier.
        settings: Loaded settings dict.  If *None*, loads from default.

    Returns:
        A tuple of ``(sentences, avg_wer)`` where *sentences* is a list
        of :class:`Sentence` models and *avg_wer* is the mean WER across
        all sentences.

    Raises:
        FileNotFoundError: If either transcript JSON is missing.
    """
    if settings is None:
        settings = load_settings()

    transcript_dir = _resolve_transcript_dir(settings)

    official_path = transcript_dir / f"{episode_id}_official.json"
    whisper_path = transcript_dir / f"{episode_id}_whisper.json"

    if not official_path.exists():
        raise FileNotFoundError(
            f"Official transcript not found for episode {episode_id}: {official_path}"
        )
    if not whisper_path.exists():
        raise FileNotFoundError(
            f"Whisper transcript not found for episode {episode_id}: {whisper_path}"
        )

    with open(official_path, "r", encoding="utf-8") as f:
        official_data = json.load(f)

    with open(whisper_path, "r", encoding="utf-8") as f:
        whisper_data = json.load(f)

    official_sentences: List[str] = official_data.get("sentences", [])
    whisper_segments: List[dict] = whisper_data.get("segments", [])

    compared = compare_sentences(official_sentences, whisper_segments)

    sentences: List[Sentence] = []
    total_wer = 0.0

    for item in compared:
        sent = Sentence(
            episode_id=episode_id,
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
    avg_wer = round(avg_wer, 4)

    logger.info(
        "Compared episode %s: %d sentences, avg WER=%.4f",
        episode_id,
        len(sentences),
        avg_wer,
    )
    return sentences, avg_wer


# ---------------------------------------------------------------------------
# Batch comparison
# ---------------------------------------------------------------------------


def compare_all(
    episode_ids: List[str],
    settings: Optional[dict] = None,
) -> List[dict]:
    """Compare transcripts for multiple episodes.

    Iterates over *episode_ids*, calling :func:`compare_episode` for each.
    Episodes with missing transcripts are logged and skipped.

    Args:
        episode_ids: List of episode identifiers.
        settings: Loaded settings dict.  If *None*, loads from default.

    Returns:
        A list of result dicts, each with keys: ``episode_id``,
        ``sentences`` (list of :class:`Sentence`), ``avg_wer``,
        ``status`` (``"done"`` | ``"skipped"`` | ``"failed"``),
        and optionally ``error``.
    """
    if settings is None:
        settings = load_settings()

    results: List[dict] = []
    total = len(episode_ids)
    done_count = 0
    skip_count = 0
    fail_count = 0

    for idx, episode_id in enumerate(episode_ids, 1):
        logger.info("Comparing episode %d/%d: %s", idx, total, episode_id)
        try:
            sentences, avg_wer = compare_episode(episode_id, settings=settings)
            results.append(
                {
                    "episode_id": episode_id,
                    "sentences": sentences,
                    "avg_wer": avg_wer,
                    "status": "done",
                }
            )
            done_count += 1
            logger.info(
                "Episode %s: done (%d sentences, avg WER=%.4f)",
                episode_id,
                len(sentences),
                avg_wer,
            )
        except FileNotFoundError as exc:
            logger.warning("Skipping %s: %s", episode_id, exc)
            results.append(
                {
                    "episode_id": episode_id,
                    "sentences": [],
                    "avg_wer": 0.0,
                    "status": "skipped",
                    "error": str(exc),
                }
            )
            skip_count += 1
        except Exception as exc:
            logger.error("Failed to compare %s: %s", episode_id, exc)
            results.append(
                {
                    "episode_id": episode_id,
                    "sentences": [],
                    "avg_wer": 0.0,
                    "status": "failed",
                    "error": str(exc),
                }
            )
            fail_count += 1

    logger.info(
        "Batch comparison complete: %d total, %d done, %d skipped, %d failed",
        total,
        done_count,
        skip_count,
        fail_count,
    )
    return results
