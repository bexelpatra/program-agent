"""Ollama client for the web-study UI (English-teacher prompt, cache-first).

Provides async ``lookup_term`` and a sync wrapper, plus ``verify_ollama_model``
for start-up model availability checks. Cache lookups use
``src.llm_cache`` against the ``abc-llm-cache`` ES index.

Design notes
------------
* Cache-first: ``llm_cache.get_cached(term, model, prompt_version, es)`` is
  consulted before any network call.
* JSON-mode: Ollama's ``/api/generate`` is called with ``format="json"`` and
  ``stream=false`` so the response is a single JSON document we can
  ``json.loads`` directly.
* Idiom etymology is required — if the model returns ``term_type == "idiom"``
  with an empty etymology, we re-prompt once with stronger wording. If it is
  still missing we persist ``etymology="(not provided)"`` and log a warning.
* Settings overrides: ``settings.llm.ollama.prompts.v1.system`` and
  ``.user_template`` take precedence over the built-in defaults.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel, Field

from . import llm_cache

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "gemma4:e2b"
DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_PROMPT_VERSION = "v1"

DEFAULT_SYSTEM_V1 = (
    "You are an expert English teacher helping Korean learners study English "
    "news. Analyze the given term and respond in valid JSON only."
)

DEFAULT_USER_TEMPLATE_V1 = (
    "Term: {term}\n"
    "Context (sentence it appeared in, may be empty): {context}\n"
    "\n"
    "Identify the term's type (one of: word, phrasal_verb, idiom, collocation) "
    "and explain it in English for an intermediate learner.\n"
    "\n"
    "Rules:\n"
    '- If type is "idiom", you MUST include an etymology explaining WHY it '
    "came to mean what it means (historical/cultural origin).\n"
    '- If type is "phrasal_verb", explain the particle\'s role.\n'
    "- Provide 2-3 example sentences (not from the context).\n"
    "- Respond with JSON only, no prose:\n"
    "{{\n"
    '  "term": "...",\n'
    '  "term_type": "word|phrasal_verb|idiom|collocation",\n'
    '  "explanation_en": "...",\n'
    '  "etymology": "... or null for non-idioms",\n'
    '  "examples": ["...", "...", "..."]\n'
    "}}"
)

IDIOM_EMPHASIS = (
    "\n\nIMPORTANT: etymology is REQUIRED for idioms. You previously omitted "
    "it — please include a concrete historical/cultural origin explaining why "
    "the phrase took on its figurative meaning."
)


# ---------------------------------------------------------------------------
# Pydantic model
# ---------------------------------------------------------------------------


class LookupResult(BaseModel):
    """Structured Ollama lookup response."""

    term: str
    term_type: str = Field(..., description="word | phrasal_verb | idiom | collocation")
    explanation_en: str
    etymology: Optional[str] = None
    examples: list[str] = Field(default_factory=list)


VALID_TERM_TYPES = {"word", "phrasal_verb", "idiom", "collocation"}


# ---------------------------------------------------------------------------
# Settings helpers
# ---------------------------------------------------------------------------


def _ollama_cfg(settings: Dict[str, Any]) -> Dict[str, Any]:
    return (settings or {}).get("llm", {}).get("ollama", {}) or {}


def _resolve_host(settings: Dict[str, Any]) -> str:
    cfg = _ollama_cfg(settings)
    return (cfg.get("host") or cfg.get("base_url") or DEFAULT_HOST).rstrip("/")


def _resolve_model(settings: Dict[str, Any]) -> str:
    return _ollama_cfg(settings).get("model") or DEFAULT_MODEL


def _resolve_timeout(settings: Dict[str, Any]) -> float:
    cfg = _ollama_cfg(settings)
    for key in ("timeout_seconds", "timeout"):
        val = cfg.get(key)
        if val is not None:
            try:
                return float(val)
            except (TypeError, ValueError):
                continue
    return float(DEFAULT_TIMEOUT_SECONDS)


def _resolve_prompt_version(settings: Dict[str, Any]) -> str:
    return _ollama_cfg(settings).get("prompt_version") or DEFAULT_PROMPT_VERSION


def _resolve_prompts(settings: Dict[str, Any], prompt_version: str) -> tuple[str, str]:
    """Return (system_prompt, user_template) with settings override support."""
    cfg = _ollama_cfg(settings)
    prompts = (cfg.get("prompts") or {}).get(prompt_version) or {}
    system = prompts.get("system") or DEFAULT_SYSTEM_V1
    user_template = prompts.get("user_template") or DEFAULT_USER_TEMPLATE_V1
    return system, user_template


def build_user_prompt(
    term: str,
    context: Optional[str],
    settings: Optional[Dict[str, Any]] = None,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
) -> str:
    """Render the user prompt for a lookup.

    ``{term}`` and ``{context}`` are substituted; any other ``{...}`` tokens
    in the template are preserved (JSON schema braces use ``{{``/``}}``).
    """
    _, user_template = _resolve_prompts(settings or {}, prompt_version)
    safe_context = context if context else ""
    # ``str.format`` would choke on the literal JSON braces unless doubled;
    # we keep the templates written with doubled braces (``{{`` / ``}}``).
    return user_template.format(term=term, context=safe_context)


def build_system_prompt(
    settings: Optional[Dict[str, Any]] = None,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
) -> str:
    system, _ = _resolve_prompts(settings or {}, prompt_version)
    return system


# ---------------------------------------------------------------------------
# HTTP call
# ---------------------------------------------------------------------------


async def _call_ollama_generate(
    host: str,
    model: str,
    system: str,
    user: str,
    timeout: float,
) -> Dict[str, Any]:
    """POST to /api/generate with JSON-mode; return parsed response dict."""
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": user,
        "system": system,
        "format": "json",
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
    raw = (data or {}).get("response", "")
    if not raw:
        raise ValueError("Ollama returned empty response body")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Ollama response was not valid JSON: {exc}: {raw!r}") from exc


def _coerce_result(term: str, parsed: Dict[str, Any]) -> LookupResult:
    """Coerce a raw dict into a ``LookupResult``, tolerant of minor drift."""
    term_type = (parsed.get("term_type") or "word").strip().lower()
    if term_type not in VALID_TERM_TYPES:
        # Best-effort remap of common aliases
        alias = {
            "phrase": "collocation",
            "phrasal": "phrasal_verb",
            "phrasalverb": "phrasal_verb",
            "phrasal-verb": "phrasal_verb",
        }.get(term_type)
        term_type = alias or "word"
    etymology = parsed.get("etymology")
    if isinstance(etymology, str) and not etymology.strip():
        etymology = None
    examples = parsed.get("examples") or []
    if isinstance(examples, str):
        examples = [examples]
    examples = [str(e) for e in examples if e]
    return LookupResult(
        term=str(parsed.get("term") or term),
        term_type=term_type,
        explanation_en=str(parsed.get("explanation_en") or "").strip(),
        etymology=etymology,
        examples=examples,
    )


# ---------------------------------------------------------------------------
# Public async API
# ---------------------------------------------------------------------------


async def lookup_term(
    term: str,
    context: Optional[str],
    settings: Dict[str, Any],
    es=None,
) -> Dict[str, Any]:
    """Look up ``term`` via Ollama with cache-first behaviour.

    Returns the response as a plain ``dict`` (the ``LookupResult.model_dump()``
    output). On cache hit, the cached dict is returned as-is.
    """
    model = _resolve_model(settings)
    prompt_version = _resolve_prompt_version(settings)

    cached = llm_cache.get_cached(term, model, prompt_version, es=es)
    if cached:
        return cached

    host = _resolve_host(settings)
    timeout = _resolve_timeout(settings)
    system = build_system_prompt(settings, prompt_version)
    user = build_user_prompt(term, context, settings, prompt_version)

    parsed = await _call_ollama_generate(host, model, system, user, timeout)
    result = _coerce_result(term, parsed)

    # Idiom etymology enforcement — one retry with emphasis.
    if result.term_type == "idiom" and not (
        result.etymology and result.etymology.strip()
    ):
        logger.info("idiom etymology missing for %r; retrying with emphasis", term)
        retry_user = user + IDIOM_EMPHASIS
        try:
            parsed_retry = await _call_ollama_generate(
                host, model, system, retry_user, timeout
            )
            retry_result = _coerce_result(term, parsed_retry)
            if retry_result.etymology and retry_result.etymology.strip():
                result = retry_result
            else:
                logger.warning(
                    "idiom etymology still missing for %r after retry; "
                    "persisting placeholder",
                    term,
                )
                result = result.model_copy(update={"etymology": "(not provided)"})
        except Exception as exc:  # pragma: no cover - network-dependent
            logger.warning(
                "idiom etymology retry failed for %r: %s; persisting placeholder",
                term,
                exc,
            )
            result = result.model_copy(update={"etymology": "(not provided)"})

    response_dict = result.model_dump()
    llm_cache.set_cached(term, model, prompt_version, response_dict, es=es)
    return response_dict


async def verify_ollama_model(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Check that the configured Ollama model is installed locally.

    Returns ``{"ok": True}`` if present, ``{"ok": False, "warning": "..."}``
    otherwise. Never raises; network issues are reported via the warning.
    """
    host = _resolve_host(settings)
    model = _resolve_model(settings)
    url = f"{host}/api/tags"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        warning = f"Could not reach Ollama at {host}: {exc}"
        logger.warning(warning)
        return {"ok": False, "warning": warning}

    models = [m.get("name") for m in (data.get("models") or []) if m.get("name")]
    if model in models:
        return {"ok": True}

    # Accept short-name prefix matches (``foo`` matches ``foo:latest``).
    for name in models:
        if name and (name == model or name.split(":", 1)[0] == model):
            return {"ok": True}

    warning = (
        f"Ollama model {model!r} not found on {host}. "
        f"Available: {models}. Lookups will fail until it is pulled."
    )
    logger.warning(warning)
    return {"ok": False, "warning": warning}


# ---------------------------------------------------------------------------
# Sync wrapper
# ---------------------------------------------------------------------------


def lookup_term_sync(
    term: str,
    context: Optional[str],
    settings: Dict[str, Any],
    es=None,
) -> Dict[str, Any]:
    """Synchronous wrapper around :func:`lookup_term` using ``asyncio.run``.

    Intended for tests and non-async callers. Do not call from within a
    running event loop — use ``await lookup_term(...)`` there instead.
    """
    return asyncio.run(lookup_term(term, context, settings, es=es))
