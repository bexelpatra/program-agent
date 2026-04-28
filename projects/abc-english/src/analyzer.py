"""spaCy-based vocabulary analysis module.

Performs POS tagging, NER-based person filtering, function-word removal,
and lemma-based word frequency analysis.  This module produces vocabulary
data only — expression/idiom extraction is handled by the LLM analyzer.

Important: LLM receives the **unfiltered** original text.  spaCy filtering
here is used exclusively for vocabulary frequency counting.
"""

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import spacy
from spacy.language import Language

from .es_client import load_settings
from .models import ExampleSentence, Vocabulary

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Project root (same convention as transcriber.py)
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Singleton model cache
# ---------------------------------------------------------------------------

_nlp: Optional[Language] = None
_nlp_model_name: Optional[str] = None


def load_nlp(settings: Optional[dict] = None) -> Language:
    """Load (or return cached) spaCy model based on settings.

    The model is cached as a module-level singleton.  If the requested
    model name differs from the currently loaded one the old model is
    discarded and the new one is loaded.

    Args:
        settings: Full settings dict (must contain a ``spacy`` section).
                  If *None*, loads from default config path.

    Returns:
        A loaded spaCy ``Language`` model instance.
    """
    global _nlp, _nlp_model_name

    if settings is None:
        settings = load_settings()

    spacy_cfg = settings.get("spacy", {})
    model_name = spacy_cfg.get("model", "en_core_web_sm")

    if _nlp is not None and _nlp_model_name == model_name:
        return _nlp

    logger.info("Loading spaCy model '%s'...", model_name)
    _nlp = spacy.load(model_name)
    _nlp_model_name = model_name
    logger.info("spaCy model '%s' loaded.", model_name)
    return _nlp


# ---------------------------------------------------------------------------
# Text analysis
# ---------------------------------------------------------------------------


def analyze_text(
    text: str,
    episode_id: str,
    settings: Optional[dict] = None,
) -> List[Vocabulary]:
    """Analyse transcript text and return vocabulary items with frequencies.

    Steps:
      1. Run spaCy pipeline (tokenisation, POS tagging, NER).
      2. Identify PERSON entities and collect their tokens for exclusion.
      3. Remove tokens whose POS is in the configured ``filter_pos`` set.
      4. Remove tokens that belong to a PERSON entity span.
      5. Aggregate remaining tokens by (lemma, pos), counting frequency and
         collecting example sentences.

    Args:
        text: Full transcript text for one episode.
        episode_id: Episode identifier (used in example sentences).
        settings: Loaded settings dict.  If *None*, loads from default path.

    Returns:
        A list of :class:`Vocabulary` objects sorted by frequency (descending).
    """
    if settings is None:
        settings = load_settings()

    nlp = load_nlp(settings)
    spacy_cfg = settings.get("spacy", {})
    filter_pos: Set[str] = set(spacy_cfg.get("filter_pos", []))
    filter_ner: Set[str] = set(spacy_cfg.get("filter_ner", ["PERSON"]))

    doc = nlp(text)

    # Build a set of token indices that belong to filtered NER entity spans
    ner_filtered_indices: Set[int] = set()
    for ent in doc.ents:
        if ent.label_ in filter_ner:
            for tok in ent:
                ner_filtered_indices.add(tok.i)

    # Map each sentence index to its text for example sentence lookup
    sent_list: List[str] = [sent.text.strip() for sent in doc.sents]

    # Build token-index → sentence-index mapping
    token_sent_map: Dict[int, int] = {}
    for sent_idx, sent in enumerate(doc.sents):
        for tok in sent:
            token_sent_map[tok.i] = sent_idx

    # Aggregate by (lemma_lower, pos)
    # value: {"frequency": int, "sentence_indices": set[int]}
    word_data: Dict[Tuple[str, str], Dict] = defaultdict(
        lambda: {"frequency": 0, "sentence_indices": set()}
    )

    for tok in doc:
        # Skip filtered POS
        if tok.pos_ in filter_pos:
            continue
        # Skip NER-filtered tokens
        if tok.i in ner_filtered_indices:
            continue
        # Skip whitespace / empty
        if tok.is_space or not tok.text.strip():
            continue

        lemma = tok.lemma_.lower().strip()
        if not lemma:
            continue

        key = (lemma, tok.pos_)
        word_data[key]["frequency"] += 1
        sent_idx = token_sent_map.get(tok.i)
        if sent_idx is not None:
            word_data[key]["sentence_indices"].add(sent_idx)

    # Convert to Vocabulary models
    vocab_list: List[Vocabulary] = []
    for (lemma, pos), data in word_data.items():
        # Pick up to 3 example sentences
        example_indices = sorted(data["sentence_indices"])[:3]
        examples = [
            ExampleSentence(episode_id=episode_id, text=sent_list[i])
            for i in example_indices
            if i < len(sent_list)
        ]

        vocab_list.append(
            Vocabulary(
                word=lemma,
                pos=pos,
                frequency=data["frequency"],
                episodes=[episode_id],
                example_sentences=examples,
            )
        )

    # Sort by frequency descending
    vocab_list.sort(key=lambda v: v.frequency, reverse=True)
    return vocab_list


# ---------------------------------------------------------------------------
# Episode-level analysis
# ---------------------------------------------------------------------------


def analyze_episode(
    episode_id: str,
    settings: Optional[dict] = None,
) -> List[Vocabulary]:
    """Analyse a single episode by loading its official transcript.

    Reads the official transcript JSON from
    ``data/transcripts/{episode_id}_official.json`` and delegates to
    :func:`analyze_text`.

    Args:
        episode_id: Unique episode identifier.
        settings: Loaded settings dict.  If *None*, loads from default path.

    Returns:
        A list of :class:`Vocabulary` objects for this episode.

    Raises:
        FileNotFoundError: If the official transcript JSON does not exist.
    """
    if settings is None:
        settings = load_settings()

    data_conf = settings.get("data", {})
    transcript_dir = data_conf.get("transcript_dir", "data/transcripts")
    transcript_path = _PROJECT_ROOT / transcript_dir / f"{episode_id}_official.json"

    if not transcript_path.exists():
        raise FileNotFoundError(
            f"Official transcript not found for episode {episode_id}: "
            f"{transcript_path}"
        )

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    full_text = transcript_data.get("full_text", "")
    if not full_text:
        # Fallback: join sentences if full_text is empty
        sentences = transcript_data.get("sentences", [])
        full_text = " ".join(sentences)

    if not full_text.strip():
        logger.warning(
            "Empty transcript for episode %s, returning empty vocabulary.",
            episode_id,
        )
        return []

    return analyze_text(full_text, episode_id, settings)


# ---------------------------------------------------------------------------
# Batch analysis
# ---------------------------------------------------------------------------


def analyze_all(
    episode_ids: List[str],
    settings: Optional[dict] = None,
) -> List[Vocabulary]:
    """Batch-analyse multiple episodes and merge vocabulary across them.

    Words with the same (lemma, pos) are merged: frequencies are summed
    and episode lists / example sentences are combined.

    Args:
        episode_ids: List of episode identifiers to process.
        settings: Loaded settings dict.  If *None*, loads from default path.

    Returns:
        A merged list of :class:`Vocabulary` objects sorted by frequency
        (descending).
    """
    if settings is None:
        settings = load_settings()

    # Merged vocab keyed by (word, pos)
    merged: Dict[Tuple[str, str], Vocabulary] = {}

    total = len(episode_ids)
    done = 0
    skipped = 0
    failed = 0

    for idx, episode_id in enumerate(episode_ids, 1):
        logger.info("Analysing episode %d/%d: %s", idx, total, episode_id)
        try:
            episode_vocab = analyze_episode(episode_id, settings)
            if not episode_vocab:
                skipped += 1
                logger.info("Episode %s: skipped (empty transcript).", episode_id)
                continue

            for v in episode_vocab:
                key = (v.word, v.pos)
                if key in merged:
                    existing = merged[key]
                    existing.frequency += v.frequency
                    # Merge episode lists (deduplicate)
                    for ep in v.episodes:
                        if ep not in existing.episodes:
                            existing.episodes.append(ep)
                    # Merge example sentences (deduplicate by episode+text)
                    existing_keys = {
                        (ex.episode_id, ex.text) for ex in existing.example_sentences
                    }
                    for ex in v.example_sentences:
                        if (ex.episode_id, ex.text) not in existing_keys:
                            existing.example_sentences.append(ex)
                            existing_keys.add((ex.episode_id, ex.text))
                else:
                    merged[key] = v.model_copy(deep=True)

            done += 1
            logger.info(
                "Episode %s: done (%d unique words).", episode_id, len(episode_vocab)
            )
        except FileNotFoundError as exc:
            failed += 1
            logger.warning("Skipping %s: %s", episode_id, exc)
        except Exception as exc:
            failed += 1
            logger.error("Failed to analyse %s: %s", episode_id, exc)

    logger.info(
        "Batch analysis complete: %d total, %d done, %d skipped, %d failed",
        total,
        done,
        skipped,
        failed,
    )

    # Sort merged results by frequency descending
    result = sorted(merged.values(), key=lambda v: v.frequency, reverse=True)
    return result
