"""Episode collector for ABC News Daily.

Crawls the ABC News Daily program page to build a list of episodes,
fetches each episode's detail page to extract metadata and determine
whether an official transcript is available, and returns a list of
Episode model instances.

The program page is a Next.js SSR app.  Episode metadata lives inside
a ``<script id="__NEXT_DATA__">`` JSON blob.  Pagination is offset-based.
"""

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .es_client import load_settings
from .models import Episode

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_crawl_config(settings: dict) -> dict:
    """Extract the ``crawling`` section from settings."""
    return settings.get("crawling", {})


def _make_session(settings: dict) -> requests.Session:
    """Create a requests Session with configured headers and retry."""
    cfg = _get_crawl_config(settings)
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": cfg.get("user_agent", "ABCEnglishStudy/1.0"),
            "Accept": "text/html,application/xhtml+xml,application/json",
            "Accept-Language": "en-AU,en;q=0.9",
        }
    )
    return session


def _request_with_retry(
    session: requests.Session,
    url: str,
    settings: dict,
) -> requests.Response:
    """GET *url* with retry and rate-limiting delay.

    Raises ``requests.HTTPError`` after exhausting retries.
    """
    cfg = _get_crawl_config(settings)
    max_retries: int = cfg.get("max_retries", 3)
    timeout: int = cfg.get("request_timeout", 30)
    delay: float = cfg.get("request_delay", 1.0)

    last_exc: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp
        except (requests.RequestException, requests.HTTPError) as exc:
            last_exc = exc
            logger.warning(
                "Request failed (attempt %d/%d) %s: %s",
                attempt,
                max_retries,
                url,
                exc,
            )
            if attempt < max_retries:
                time.sleep(delay * attempt)  # linear back-off

    raise last_exc  # type: ignore[misc]


def _extract_next_data(html: str) -> dict:
    """Parse the ``__NEXT_DATA__`` JSON blob from an HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("script", id="__NEXT_DATA__")
    if tag is None or tag.string is None:
        raise ValueError("__NEXT_DATA__ script tag not found on page")
    return json.loads(tag.string)


# ---------------------------------------------------------------------------
# Episode list (pagination)
# ---------------------------------------------------------------------------


def fetch_episode_list(settings: dict) -> List[Dict[str, Any]]:
    """Fetch the full list of episodes via paginated requests.

    Each page is loaded by appending ``?offset=N`` to the program URL.
    The function keeps paginating until no new items are returned.

    Returns:
        A list of dicts, each containing at minimum ``url`` and basic
        metadata as found in ``__NEXT_DATA__``.
    """
    cfg = _get_crawl_config(settings)
    base_url: str = cfg.get("base_url", "https://www.abc.net.au")
    program_url: str = cfg.get(
        "program_url",
        "https://www.abc.net.au/listen/programs/abc-news-daily",
    )
    delay: float = cfg.get("request_delay", 1.0)

    session = _make_session(settings)
    all_episodes: List[Dict[str, Any]] = []
    seen_ids: set = set()
    offset = 0
    page_size = 10  # typical ABC page size

    while True:
        url = program_url if offset == 0 else f"{program_url}?offset={offset}"
        logger.info("Fetching episode list page offset=%d", offset)

        resp = _request_with_retry(session, url, settings)
        next_data = _extract_next_data(resp.text)

        # Navigate the __NEXT_DATA__ structure to find episode items.
        # The exact path may vary; we try common patterns.
        items = _extract_items_from_next_data(next_data)

        if not items:
            logger.info("No more episodes at offset=%d, stopping.", offset)
            break

        new_count = 0
        for item in items:
            ep_id = _extract_episode_id(item)
            if ep_id and ep_id not in seen_ids:
                seen_ids.add(ep_id)
                ep_url = _build_episode_url(item, base_url)
                all_episodes.append(
                    {
                        "episode_id": ep_id,
                        "title": _deep_get(item, "title", default=""),
                        "description": _deep_get(item, "description", default=""),
                        "published_date": _deep_get(item, "publishedDate", default=""),
                        "duration_seconds": _deep_get(item, "duration", default=0),
                        "url": ep_url,
                        "audio_url": _extract_audio_url(item),
                    }
                )
                new_count += 1

        if new_count == 0:
            logger.info("No new episodes found at offset=%d, stopping.", offset)
            break

        offset += page_size
        time.sleep(delay)

    logger.info("Collected %d episodes total.", len(all_episodes))
    return all_episodes


# ---------------------------------------------------------------------------
# __NEXT_DATA__ navigation helpers
# ---------------------------------------------------------------------------


def _extract_items_from_next_data(data: dict) -> List[dict]:
    """Walk the __NEXT_DATA__ JSON to find episode item list.

    ABC's Next.js payload varies but episodes typically live under:
      props.pageProps.data.program.episodes.items
    or
      props.pageProps.data.items
    or
      props.pageProps.episodes

    This function tries several known paths and returns the first
    non-empty list found.
    """
    paths = [
        ["props", "pageProps", "data", "program", "episodes", "items"],
        ["props", "pageProps", "data", "items"],
        ["props", "pageProps", "episodes"],
        ["props", "pageProps", "data", "episodes"],
        ["props", "pageProps", "data", "program", "items"],
    ]
    for path in paths:
        node = data
        for key in path:
            if isinstance(node, dict):
                node = node.get(key)
            else:
                node = None
                break
        if isinstance(node, list) and len(node) > 0:
            return node
    return []


def _extract_episode_id(item: dict) -> Optional[str]:
    """Extract a unique episode ID from a list-page item dict."""
    # Try direct id field
    for key in ("id", "episodeId", "episode_id"):
        val = item.get(key)
        if val is not None:
            return str(val)

    # Try extracting from a URL/slug field
    link = item.get("link") or item.get("url") or item.get("slug", "")
    if link:
        parts = str(link).rstrip("/").split("/")
        if parts and parts[-1].isdigit():
            return parts[-1]

    return None


def _build_episode_url(item: dict, base_url: str) -> str:
    """Build a full episode URL from an item dict."""
    link = item.get("link") or item.get("url") or ""
    link = str(link)
    if link.startswith("http"):
        return link
    if link.startswith("/"):
        return f"{base_url}{link}"

    # Construct from slug / id
    slug = item.get("slug", "")
    ep_id = _extract_episode_id(item) or ""
    if slug and ep_id:
        return f"{base_url}/listen/programs/abc-news-daily/{slug}/{ep_id}"
    if ep_id:
        return f"{base_url}/listen/programs/abc-news-daily/{ep_id}"
    return ""


def _extract_audio_url(item: dict) -> str:
    """Try to extract the MP3 URL from a list-page item."""
    for key in ("audioUrl", "audio_url", "mediaUrl", "audio"):
        val = item.get(key)
        if val and isinstance(val, str):
            return val

    # May be nested under a 'media' dict
    media = item.get("media") or item.get("audio") or {}
    if isinstance(media, dict):
        return media.get("url", "") or media.get("mp3", "")

    return ""


def _deep_get(d: dict, key: str, default: Any = None) -> Any:
    """Get a value by key, also trying snake_case variant."""
    if key in d:
        return d[key]
    # Try snake_case
    snake = "".join(f"_{c.lower()}" if c.isupper() else c for c in key)
    return d.get(snake, default)


# ---------------------------------------------------------------------------
# Episode detail
# ---------------------------------------------------------------------------


def fetch_episode_detail(url: str, settings: dict) -> Dict[str, Any]:
    """Fetch a single episode page and extract metadata + transcript status.

    Args:
        url: Full URL of the episode page.
        settings: Loaded settings dict.

    Returns:
        A dict with episode metadata.  The ``has_transcript`` key is True
        only when a ``div#transcript`` (or any element with id="transcript")
        is present on the page.
    """
    session = _make_session(settings)
    resp = _request_with_retry(session, url, settings)
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # -- transcript presence --
    has_transcript = soup.find(id="transcript") is not None

    # -- __NEXT_DATA__ for structured metadata --
    # Store raw HTML so callers can pass it to parse_transcript without
    # making a second HTTP request.
    result: Dict[str, Any] = {
        "url": url,
        "has_transcript": has_transcript,
        "_html": html,
    }

    try:
        next_data = _extract_next_data(html)
        episode_data = _extract_episode_from_detail(next_data)
        if episode_data:
            result["episode_id"] = str(
                episode_data.get("id", "") or episode_data.get("episodeId", "")
            )
            result["title"] = episode_data.get("title", "")
            result["description"] = episode_data.get("description", "")
            result["published_date"] = episode_data.get(
                "publishedDate", ""
            ) or episode_data.get("published_date", "")
            result["duration_seconds"] = episode_data.get(
                "duration", 0
            ) or episode_data.get("duration_seconds", 0)
            result["audio_url"] = _extract_audio_url(episode_data)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        logger.warning("Could not parse __NEXT_DATA__ for %s: %s", url, exc)

    # Fallback: extract episode_id from URL
    if not result.get("episode_id"):
        parts = url.rstrip("/").split("/")
        if parts and parts[-1].isdigit():
            result["episode_id"] = parts[-1]

    return result


def _extract_episode_from_detail(data: dict) -> Optional[dict]:
    """Extract episode dict from a detail page's __NEXT_DATA__."""
    paths = [
        ["props", "pageProps", "data", "episode"],
        ["props", "pageProps", "episode"],
        ["props", "pageProps", "data", "item"],
        ["props", "pageProps", "data"],
    ]
    for path in paths:
        node = data
        for key in path:
            if isinstance(node, dict):
                node = node.get(key)
            else:
                node = None
                break
        if isinstance(node, dict) and ("title" in node or "id" in node):
            return node
    return None


# ---------------------------------------------------------------------------
# Transcript parsing
# ---------------------------------------------------------------------------


def parse_transcript(html_content: str) -> dict:
    """Extract transcript text from the ``div#transcript`` element.

    Parses the HTML, strips tags, normalises whitespace, and splits the
    text into individual sentences (splitting on ``./!/?``).

    Args:
        html_content: Full HTML of an episode page.

    Returns:
        A dict with keys ``full_text`` (str) and ``sentences`` (list[str]).
        Returns empty values when no transcript element is found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    transcript_el = soup.find(id="transcript")

    if transcript_el is None:
        return {"full_text": "", "sentences": []}

    # Get text, collapsing whitespace but preserving paragraph breaks
    raw_text = transcript_el.get_text(separator=" ", strip=True)
    # Normalise whitespace
    full_text = re.sub(r"\s+", " ", raw_text).strip()

    if not full_text:
        return {"full_text": "", "sentences": []}

    # Split on sentence-ending punctuation, keeping the punctuation attached
    # e.g. "Hello world. How are you? Fine!" -> ["Hello world.", "How are you?", "Fine!"]
    raw_sentences = re.split(r"(?<=[.!?])\s+", full_text)
    sentences = [s.strip() for s in raw_sentences if s.strip()]

    return {"full_text": full_text, "sentences": sentences}


def save_transcript(
    episode_id: str,
    transcript_data: dict,
    settings: dict,
) -> str:
    """Save parsed transcript data as a JSON file.

    File is written to ``{data.transcript_dir}/{episode_id}_official.json``.

    Args:
        episode_id: Unique episode identifier.
        transcript_data: Dict from :func:`parse_transcript`.
        settings: Loaded settings dict.

    Returns:
        Absolute path to the saved JSON file.
    """
    data_conf = settings.get("data", {})
    transcript_dir = data_conf.get("transcript_dir", "data/transcripts")

    # Resolve relative to project root (parent of src/)
    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / transcript_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{episode_id}_official.json"
    payload = {
        "episode_id": episode_id,
        "sentences": transcript_data.get("sentences", []),
        "full_text": transcript_data.get("full_text", ""),
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    logger.info("Saved transcript for %s → %s", episode_id, out_path)
    return str(out_path)


# ---------------------------------------------------------------------------
# MP3 download
# ---------------------------------------------------------------------------


def download_mp3(
    episode_id: str,
    audio_url: str,
    settings: dict,
) -> str:
    """Download an MP3 file with progress bar and duplicate prevention.

    The file is saved to ``{data.audio_dir}/{episode_id}.mp3``.  If the
    file already exists the download is skipped.

    Args:
        episode_id: Unique episode identifier.
        audio_url: Direct URL to the MP3 resource.
        settings: Loaded settings dict.

    Returns:
        Absolute path to the MP3 file (whether newly downloaded or existing).
    """
    data_conf = settings.get("data", {})
    audio_dir = data_conf.get("audio_dir", "data/audio")

    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / audio_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    out_path = out_dir / f"{episode_id}.mp3"

    # Duplicate prevention
    if out_path.exists():
        logger.info("MP3 already exists, skipping: %s", out_path)
        return str(out_path)

    if not audio_url:
        logger.warning("No audio URL for episode %s, skipping download.", episode_id)
        return ""

    session = _make_session(settings)
    cfg = _get_crawl_config(settings)
    timeout = cfg.get("request_timeout", 30)

    logger.info("Downloading MP3 for %s from %s", episode_id, audio_url)
    resp = session.get(audio_url, stream=True, timeout=timeout)
    resp.raise_for_status()

    total_size = int(resp.headers.get("content-length", 0))
    tmp_path = out_path.with_suffix(".mp3.tmp")

    try:
        with (
            open(tmp_path, "wb") as f,
            tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=f"MP3 {episode_id}",
                disable=total_size == 0,
            ) as pbar,
        ):
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

        # Atomic-ish rename
        tmp_path.rename(out_path)
        logger.info("Downloaded MP3 → %s", out_path)
    except Exception:
        # Clean up partial file on failure
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    return str(out_path)


# ---------------------------------------------------------------------------
# Full collection pipeline
# ---------------------------------------------------------------------------


def collect_all(settings: Optional[dict] = None) -> List[Episode]:
    """Run the full collection pipeline.

    1. Fetch the paginated episode list.
    2. For each episode, fetch the detail page to confirm metadata and
       determine transcript availability.
    3. For episodes with a transcript: parse it and save as JSON.
    4. For episodes with a transcript and audio URL: download the MP3.
    5. Return a list of :class:`Episode` model instances.

    Args:
        settings: Loaded settings dict.  If None, loads from default path.

    Returns:
        List of Episode instances (includes both has_transcript=True and False).
    """
    if settings is None:
        settings = load_settings()

    cfg = _get_crawl_config(settings)
    delay: float = cfg.get("request_delay", 1.0)

    logger.info("Starting episode collection...")
    raw_list = fetch_episode_list(settings)

    episodes: List[Episode] = []
    for idx, raw in enumerate(raw_list, 1):
        ep_url = raw.get("url", "")
        if not ep_url:
            logger.warning("Skipping episode with no URL: %s", raw)
            continue

        logger.info(
            "Fetching detail %d/%d: %s", idx, len(raw_list), raw.get("title", "")
        )

        try:
            detail = fetch_episode_detail(ep_url, settings)
            detail_html = detail.pop("_html", "")
        except Exception as exc:
            logger.error("Failed to fetch detail for %s: %s", ep_url, exc)
            # Use list-page data as fallback, mark transcript unknown
            detail = {**raw, "has_transcript": False}
            detail_html = ""

        # Merge list-page data with detail-page data (detail takes precedence)
        merged = {**raw, **detail}

        # Parse published_date
        published = merged.get("published_date", "")
        from datetime import datetime

        if isinstance(published, str) and published:
            for fmt in (
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
            ):
                try:
                    published = datetime.strptime(published, fmt)
                    break
                except ValueError:
                    continue
            else:
                published = datetime.utcnow()
        elif not isinstance(published, datetime):
            published = datetime.utcnow()

        has_transcript = merged.get("has_transcript", False)
        episode_id = merged.get("episode_id", "")
        audio_url = merged.get("audio_url", "")
        official_transcript = ""

        # --- Transcript parsing (only for episodes with transcript) ---
        if has_transcript and detail_html and episode_id:
            try:
                transcript_data = parse_transcript(detail_html)
                if transcript_data["full_text"]:
                    save_transcript(episode_id, transcript_data, settings)
                    official_transcript = transcript_data["full_text"]
                    logger.info(
                        "Parsed transcript for %s: %d sentences",
                        episode_id,
                        len(transcript_data["sentences"]),
                    )
                else:
                    logger.warning(
                        "Transcript element found but empty for %s", episode_id
                    )
            except Exception as exc:
                logger.error("Failed to parse transcript for %s: %s", episode_id, exc)

        # --- MP3 download (only for episodes with transcript) ---
        if has_transcript and audio_url and episode_id:
            try:
                download_mp3(episode_id, audio_url, settings)
            except Exception as exc:
                logger.error("Failed to download MP3 for %s: %s", episode_id, exc)

        episode = Episode(
            episode_id=episode_id,
            title=merged.get("title", ""),
            description=merged.get("description", ""),
            published_date=published,
            duration_seconds=int(merged.get("duration_seconds", 0) or 0),
            url=merged.get("url", ""),
            audio_url=audio_url,
            has_transcript=has_transcript,
            official_transcript=official_transcript,
        )
        episodes.append(episode)

        if idx < len(raw_list):
            time.sleep(delay)

    with_transcript = sum(1 for e in episodes if e.has_transcript)
    logger.info(
        "Collection complete: %d episodes (%d with transcript, %d without)",
        len(episodes),
        with_transcript,
        len(episodes) - with_transcript,
    )
    return episodes
