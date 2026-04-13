"""LLM-based deep analysis module.

Provides a provider abstraction layer for LLM interactions, supporting
Anthropic (Claude) and local Ollama models.  The active provider is
selected via settings.yaml ``llm.provider``.

Also contains analysis functions for detecting idioms, phrasal verbs,
and collocations in text, with etymology explanations.
"""

import hashlib
import json
import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

import requests as http_requests

from .es_client import load_settings
from .models import Expression, ExampleSentence

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, prompt: str, system: str = "") -> str:
        """Generate a text completion.

        Args:
            prompt: The user prompt.
            system: Optional system prompt.

        Returns:
            The generated text response.
        """

    def generate_json(self, prompt: str, system: str = "") -> dict:
        """Generate a completion and parse the response as JSON.

        Attempts to extract a JSON object from the response.  Looks for
        a fenced ``json`` code block first; if not found, tries to parse
        the entire response.

        Args:
            prompt: The user prompt.
            system: Optional system prompt.

        Returns:
            Parsed JSON as a Python dict.

        Raises:
            ValueError: If the response cannot be parsed as JSON.
        """
        raw = self.generate(prompt, system)
        return _extract_json(raw)


# ---------------------------------------------------------------------------
# JSON extraction helper
# ---------------------------------------------------------------------------

_JSON_BLOCK_RE = re.compile(r"```json\s*\n?(.*?)\n?\s*```", re.DOTALL)


def _extract_json(text: str) -> dict:
    """Extract and parse JSON from an LLM response string.

    Tries fenced ``json`` blocks first, then the whole text.

    Args:
        text: Raw LLM response.

    Returns:
        Parsed dict.

    Raises:
        ValueError: On parse failure.
    """
    # Try fenced json block
    match = _JSON_BLOCK_RE.search(text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass  # fall through to whole-text attempt

    # Try whole text
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Failed to parse JSON from LLM response. "
            f"Response (first 500 chars): {text[:500]}"
        ) from exc


# ---------------------------------------------------------------------------
# Anthropic provider
# ---------------------------------------------------------------------------


class AnthropicProvider(LLMProvider):
    """LLM provider backed by the Anthropic Messages API (Claude)."""

    def __init__(self, settings: dict) -> None:
        import anthropic

        llm_cfg = settings.get("llm", {}).get("anthropic", {})
        self.model = llm_cfg.get("model", "claude-3-haiku-20240307")
        self.max_tokens = llm_cfg.get("max_tokens", 4096)

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set.")

        self._client = anthropic.Anthropic(api_key=api_key)
        logger.info(
            "AnthropicProvider initialised (model=%s, max_tokens=%d)",
            self.model,
            self.max_tokens,
        )

    def generate(self, prompt: str, system: str = "") -> str:
        """Call the Anthropic Messages API and return the text response."""
        kwargs: dict = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)
        # Extract text from content blocks
        return "".join(block.text for block in response.content if block.type == "text")


# ---------------------------------------------------------------------------
# Ollama provider
# ---------------------------------------------------------------------------


class OllamaProvider(LLMProvider):
    """LLM provider backed by a local Ollama instance."""

    def __init__(self, settings: dict) -> None:
        llm_cfg = settings.get("llm", {}).get("ollama", {})
        self.model = llm_cfg.get("model", "llama3")
        self.base_url = llm_cfg.get("base_url", "http://localhost:11434").rstrip("/")
        logger.info(
            "OllamaProvider initialised (model=%s, base_url=%s)",
            self.model,
            self.base_url,
        )

    def generate(self, prompt: str, system: str = "") -> str:
        """Call the Ollama REST API and return the generated text."""
        payload: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system

        url = f"{self.base_url}/api/generate"
        resp = http_requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")


# ---------------------------------------------------------------------------
# Provider factory (singleton)
# ---------------------------------------------------------------------------

_provider: Optional[LLMProvider] = None
_provider_name: Optional[str] = None


def get_provider(settings: Optional[dict] = None) -> LLMProvider:
    """Return the configured LLM provider (singleton).

    The provider type is determined by ``settings['llm']['provider']``.
    Once created, the same instance is returned on subsequent calls
    unless :func:`reset_provider` is called.

    Args:
        settings: Full settings dict.  If None, loads from the default
                  config path.

    Returns:
        An :class:`LLMProvider` instance.

    Raises:
        ValueError: If the configured provider name is not recognised.
    """
    global _provider, _provider_name

    if settings is None:
        settings = load_settings()

    llm_cfg = settings.get("llm", {})
    name = llm_cfg.get("provider", "anthropic")

    if _provider is not None and _provider_name == name:
        return _provider

    if name == "anthropic":
        _provider = AnthropicProvider(settings)
    elif name == "ollama":
        _provider = OllamaProvider(settings)
    else:
        raise ValueError(f"Unknown LLM provider '{name}'. Supported: anthropic, ollama")

    _provider_name = name
    return _provider


def reset_provider() -> None:
    """Reset the singleton provider (useful for testing or reconfiguration)."""
    global _provider, _provider_name
    _provider = None
    _provider_name = None


# ---------------------------------------------------------------------------
# LLM response caching
# ---------------------------------------------------------------------------

_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "cache" / "llm"


def _make_cache_key(prefix: str, content: str) -> str:
    """Create a hash-based cache key from a prefix and content string.

    Args:
        prefix: A short label such as ``"expressions"`` or ``"vocabulary"``.
        content: The text whose hash forms the unique part of the key.

    Returns:
        A string of the form ``"{prefix}_{sha256_hex}"``.
    """
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"{prefix}_{digest}"


def _get_cache(cache_key: str) -> Optional[dict]:
    """Look up a cached LLM response.

    Args:
        cache_key: Key returned by :func:`_make_cache_key`.

    Returns:
        The cached dict/list, or *None* on cache miss.
    """
    path = _CACHE_DIR / f"{cache_key}.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                logger.debug("Cache hit: %s", cache_key)
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupt cache file, ignoring: %s", path)
    return None


def _set_cache(cache_key: str, data) -> None:
    """Persist an LLM response to the file-based cache.

    Args:
        cache_key: Key returned by :func:`_make_cache_key`.
        data: JSON-serialisable object (dict or list).
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _CACHE_DIR / f"{cache_key}.json"
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        logger.debug("Cache saved: %s", cache_key)
    except OSError as exc:
        logger.warning("Failed to write cache file %s: %s", path, exc)


# ---------------------------------------------------------------------------
# Text batching helpers
# ---------------------------------------------------------------------------

_LONG_TEXT_WORD_THRESHOLD = 5000


def _split_text_into_chunks(
    text: str, max_words: int = _LONG_TEXT_WORD_THRESHOLD
) -> List[str]:
    """Split *text* into chunks of roughly *max_words* words each.

    Splitting is done at sentence boundaries (periods followed by a space or
    newline) to avoid cutting in the middle of a sentence whenever possible.

    Args:
        text: The text to split.
        max_words: Target maximum number of words per chunk.

    Returns:
        A list of text chunks.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: List[str] = []
    current_chunk: List[str] = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current_word_count + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(sentence)
        current_word_count += word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def _merge_expression_results(results_list: List[List[dict]]) -> List[dict]:
    """Merge expression results from multiple chunks, removing duplicates.

    Duplicates are identified by normalised (lowercased, stripped) phrase.

    Args:
        results_list: List of per-chunk expression result lists.

    Returns:
        De-duplicated list of expression dicts.
    """
    seen: set = set()
    merged: List[dict] = []
    for results in results_list:
        for item in results:
            phrase_key = item.get("phrase", "").strip().lower()
            if phrase_key and phrase_key not in seen:
                seen.add(phrase_key)
                merged.append(item)
    return merged


# ---------------------------------------------------------------------------
# Expression detection (idioms, phrasal verbs, collocations)
# ---------------------------------------------------------------------------

_EXPRESSION_SYSTEM_PROMPT = (
    "You are an expert English linguist specialising in idioms, phrasal verbs, "
    "and collocations.  You also have deep knowledge of etymology and the "
    "historical origins of English expressions.  Respond ONLY with valid JSON."
)

_EXPRESSION_USER_PROMPT_TEMPLATE = """\
Analyse the following English text and identify ALL idioms, phrasal verbs, \
and collocations present.

For each expression found, return a JSON object with these fields:
- "phrase": the expression as it appears in the text
- "type": one of "idiom", "phrasal_verb", or "collocation"
- "definition_en": concise English definition
- "definition_ko": Korean translation / definition
- "etymology": explain the origin and why the expression has this meaning \
(2-4 sentences)
- "difficulty": CEFR level (one of A1, A2, B1, B2, C1, C2)

Return the results as a JSON array (a list of objects).  If none are found, \
return an empty array [].

Text:
\"\"\"
{text}
\"\"\"
"""


def _parse_expression_result(result) -> List[dict]:
    """Normalise the LLM response for expression detection into a list of dicts."""
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        for key in ("expressions", "results", "items", "data"):
            if key in result and isinstance(result[key], list):
                return result[key]
        if "phrase" in result:
            return [result]
    return []


def detect_expressions(text: str, settings: dict = None) -> List[dict]:
    """Detect idioms, phrasal verbs, and collocations in *text* using LLM.

    The full original text is sent to the LLM without any preprocessing
    (no stop-word or NER filtering) so that multi-word expressions are
    preserved intact.

    For very long texts (over 5 000 words) the text is split into chunks,
    each chunk is analysed separately, and the results are merged with
    duplicate removal.

    Results are cached on disk so that re-analysing the same text does not
    trigger additional LLM API calls.

    Args:
        text: The raw English text to analyse.
        settings: Optional settings dict.  If *None*, loads defaults.

    Returns:
        A list of dicts, each containing keys ``phrase``, ``type``,
        ``definition_en``, ``definition_ko``, ``etymology``, ``difficulty``.
    """
    # --- cache check ---
    cache_key = _make_cache_key("expressions", text)
    cached = _get_cache(cache_key)
    if cached is not None:
        logger.info("Using cached expression results (%d items)", len(cached))
        return cached

    provider = get_provider(settings)

    # --- batch splitting for long texts ---
    word_count = len(text.split())
    if word_count > _LONG_TEXT_WORD_THRESHOLD:
        chunks = _split_text_into_chunks(text)
        logger.info(
            "Text has %d words; split into %d chunks for expression detection",
            word_count,
            len(chunks),
        )
        chunk_results: List[List[dict]] = []
        for idx, chunk in enumerate(chunks):
            user_prompt = _EXPRESSION_USER_PROMPT_TEMPLATE.format(text=chunk)
            try:
                result = provider.generate_json(
                    user_prompt, system=_EXPRESSION_SYSTEM_PROMPT
                )
                chunk_results.append(_parse_expression_result(result))
            except ValueError:
                logger.error("Failed to parse LLM JSON for chunk %d", idx)
                chunk_results.append([])
        merged = _merge_expression_results(chunk_results)
        _set_cache(cache_key, merged)
        return merged

    # --- single-call path ---
    user_prompt = _EXPRESSION_USER_PROMPT_TEMPLATE.format(text=text)
    result = provider.generate_json(user_prompt, system=_EXPRESSION_SYSTEM_PROMPT)
    expressions = _parse_expression_result(result)

    _set_cache(cache_key, expressions)
    return expressions


def detect_expressions_for_episode(
    episode_id: str, settings: dict = None
) -> List[Expression]:
    """Detect expressions in an episode's official transcript.

    Loads the official transcript JSON from
    ``data/transcripts/{episode_id}_official.json``, sends the full text
    to :func:`detect_expressions`, and converts the raw dicts into
    :class:`Expression` model instances.

    Args:
        episode_id: The episode identifier (e.g. ``"106551254"``).
        settings: Optional settings dict.

    Returns:
        A list of :class:`Expression` instances.
    """
    project_root = Path(__file__).resolve().parent.parent
    transcript_path = (
        project_root / "data" / "transcripts" / f"{episode_id}_official.json"
    )

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    # The official transcript JSON format is:
    #   {"episode_id": "...", "sentences": [...], "full_text": "..."}
    if isinstance(transcript_data, str):
        text = transcript_data
    elif isinstance(transcript_data, dict):
        text = transcript_data.get("full_text") or " ".join(
            transcript_data.get("sentences", [])
        )
    else:
        text = str(transcript_data)

    raw_expressions = detect_expressions(text, settings=settings)

    expressions: List[Expression] = []
    for item in raw_expressions:
        expr_type = item.get("type", "collocation")
        # Normalise type value (e.g. "phrasal verb" -> "phrasal_verb")
        expr_type = expr_type.replace(" ", "_").lower()
        if expr_type not in ("idiom", "phrasal_verb", "collocation"):
            expr_type = "collocation"

        expressions.append(
            Expression(
                phrase=item.get("phrase", ""),
                type=expr_type,
                definition_en=item.get("definition_en", ""),
                definition_ko=item.get("definition_ko", ""),
                etymology=item.get("etymology", ""),
                difficulty=item.get("difficulty", ""),
                frequency=1,
                episodes=[episode_id],
                example_sentences=[],
            )
        )

    logger.info("Detected %d expressions for episode %s", len(expressions), episode_id)
    return expressions


# ---------------------------------------------------------------------------
# Vocabulary CEFR classification + Korean definitions
# ---------------------------------------------------------------------------


def _get_batch_size(settings: Optional[dict] = None) -> int:
    """Return the configured batch size for the active LLM provider."""
    if settings is None:
        settings = load_settings()
    llm_cfg = settings.get("llm", {})
    provider_name = llm_cfg.get("provider", "anthropic")
    return llm_cfg.get(provider_name, {}).get("batch_size", 10)


def classify_vocabulary(
    words: List[str], text: str, settings: Optional[dict] = None
) -> List[dict]:
    """Classify words by CEFR difficulty and provide English/Korean definitions.

    Sends the full original text together with a list of words to the LLM
    so that definitions are context-aware.  Words are processed in batches
    according to the ``batch_size`` setting for the active provider.

    Args:
        words: List of words to classify.
        text: The full original transcript text (provides context).
        settings: Optional pre-loaded settings dict.

    Returns:
        A list of dicts, each containing ``word``, ``difficulty``,
        ``definition_en``, and ``definition_ko``.
    """
    if not words:
        return []

    if settings is None:
        settings = load_settings()

    # --- cache check (key combines words + context text) ---
    cache_content = json.dumps(sorted(words), ensure_ascii=False) + "\n" + text
    cache_key = _make_cache_key("vocabulary", cache_content)
    cached = _get_cache(cache_key)
    if cached is not None:
        logger.info("Using cached vocabulary classification (%d items)", len(cached))
        return cached

    provider = get_provider(settings)
    batch_size = _get_batch_size(settings)

    system_prompt = (
        "You are an English education expert and CEFR classification specialist. "
        "For each word provided, determine its CEFR level (A1, A2, B1, B2, C1, C2) "
        "based on the context in which it appears, provide a concise English definition "
        "that reflects its contextual meaning, and provide a Korean translation. "
        "Respond ONLY with a JSON array."
    )

    all_results: List[dict] = []

    for i in range(0, len(words), batch_size):
        batch = words[i : i + batch_size]
        word_list_str = ", ".join(f'"{w}"' for w in batch)

        user_prompt = (
            f"Here is the full text for context:\n\n---\n{text}\n---\n\n"
            f"Classify the following words: [{word_list_str}]\n\n"
            "For each word, return a JSON array of objects with these fields:\n"
            '- "word": the word\n'
            '- "difficulty": CEFR level (A1, A2, B1, B2, C1, C2)\n'
            '- "definition_en": concise English definition based on context\n'
            '- "definition_ko": Korean translation\n\n'
            "Return ONLY the JSON array, no other text."
        )

        try:
            parsed = provider.generate_json(user_prompt, system=system_prompt)
        except ValueError:
            logger.error("Failed to parse LLM JSON for batch starting at index %d", i)
            for w in batch:
                all_results.append(
                    {
                        "word": w,
                        "difficulty": "",
                        "definition_en": "",
                        "definition_ko": "",
                    }
                )
            continue

        # The LLM may return {"words": [...]} instead of a plain list.
        if isinstance(parsed, dict):
            for key in ("words", "results", "vocabulary"):
                if key in parsed and isinstance(parsed[key], list):
                    parsed = parsed[key]
                    break
            else:
                # Last resort: take the first list value found
                for v in parsed.values():
                    if isinstance(v, list):
                        parsed = v
                        break

        if isinstance(parsed, list):
            all_results.extend(parsed)
        else:
            logger.warning("Unexpected LLM response structure for batch at index %d", i)
            for w in batch:
                all_results.append(
                    {
                        "word": w,
                        "difficulty": "",
                        "definition_en": "",
                        "definition_ko": "",
                    }
                )

    # --- save to cache ---
    _set_cache(cache_key, all_results)
    return all_results


def classify_vocabulary_for_episode(
    episode_id: str, vocabulary: List, settings: Optional[dict] = None
) -> List[dict]:
    """Classify vocabulary items for a specific episode.

    Loads the official transcript for *episode_id*, extracts words from the
    *vocabulary* list, calls :func:`classify_vocabulary`, and merges the
    results (difficulty, definition_en, definition_ko) back into the
    vocabulary items.

    Args:
        episode_id: The episode identifier used to locate the transcript JSON
            file under ``data/transcripts/``.
        vocabulary: A list of dicts (or objects with a ``word`` attribute)
            representing vocabulary items.
        settings: Optional pre-loaded settings dict.

    Returns:
        The *vocabulary* list with ``difficulty``, ``definition_en``, and
        ``definition_ko`` fields updated from the LLM classification.
    """
    if not vocabulary:
        return []

    # Load official transcript
    project_root = Path(__file__).resolve().parent.parent
    transcript_path = (
        project_root / "data" / "transcripts" / f"{episode_id}_official.json"
    )

    if not transcript_path.exists():
        logger.error("Transcript file not found: %s", transcript_path)
        return vocabulary

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    # The official transcript JSON format is:
    #   {"episode_id": "...", "sentences": [...], "full_text": "..."}
    text = transcript_data.get("full_text") or " ".join(
        transcript_data.get("sentences", [])
    )
    if not text:
        logger.error("No full_text or sentences field in %s", transcript_path)
        return vocabulary

    # Extract words from vocabulary items
    words: List[str] = []
    for item in vocabulary:
        if isinstance(item, dict):
            words.append(item.get("word", ""))
        else:
            words.append(getattr(item, "word", ""))

    classified = classify_vocabulary(words, text, settings=settings)

    # Build a lookup by word (lowercase) for merging
    lookup: dict = {}
    for entry in classified:
        if isinstance(entry, dict):
            w = entry.get("word", "").lower()
            if w:
                lookup[w] = entry

    # Merge results back into vocabulary
    result: List[dict] = []
    for item in vocabulary:
        if isinstance(item, dict):
            item_dict = dict(item)
            word_key = item_dict.get("word", "").lower()
        else:
            item_dict = (
                item.model_dump()
                if hasattr(item, "model_dump")
                else item.__dict__.copy()
            )
            word_key = getattr(item, "word", "").lower()

        if word_key in lookup:
            match = lookup[word_key]
            item_dict["difficulty"] = match.get("difficulty", "")
            item_dict["definition_en"] = match.get("definition_en", "")
            item_dict["definition_ko"] = match.get("definition_ko", "")

        result.append(item_dict)

    return result
