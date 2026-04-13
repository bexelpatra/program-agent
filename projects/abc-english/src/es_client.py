"""Elasticsearch connection management module.

Reads connection settings from config/settings.yaml and provides
a singleton-like ES client for use across the pipeline.
"""

from pathlib import Path
from typing import Optional

import yaml
from elasticsearch import Elasticsearch


_DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "settings.yaml"
)

_client: Optional[Elasticsearch] = None


def load_settings(config_path: Optional[Path] = None) -> dict:
    """Load settings from the YAML configuration file.

    Args:
        config_path: Path to settings.yaml. Defaults to config/settings.yaml
                     relative to the project root.

    Returns:
        Parsed settings dictionary.

    Raises:
        FileNotFoundError: If the config file does not exist.
    """
    path = config_path or _DEFAULT_CONFIG_PATH
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_es_config(settings: Optional[dict] = None) -> dict:
    """Extract Elasticsearch configuration from settings.

    Args:
        settings: Full settings dict. If None, loads from default path.

    Returns:
        Dict with keys: host, port, scheme, indices, bulk_size.
    """
    if settings is None:
        settings = load_settings()
    return settings.get("elasticsearch", {})


def get_client(
    config_path: Optional[Path] = None,
    settings: Optional[dict] = None,
) -> Elasticsearch:
    """Get or create the Elasticsearch client (singleton).

    On first call, creates a new client using settings from the config file.
    Subsequent calls return the same client instance unless ``reset_client``
    is called first.

    Args:
        config_path: Path to settings.yaml (used only on first creation).
        settings: Pre-loaded settings dict (takes precedence over config_path).

    Returns:
        Connected Elasticsearch client instance.
    """
    global _client
    if _client is not None:
        return _client

    if settings is None:
        settings = load_settings(config_path)

    es_conf = get_es_config(settings)
    host = es_conf.get("host", "localhost")
    port = es_conf.get("port", 9200)
    scheme = es_conf.get("scheme", "http")

    _client = Elasticsearch(
        hosts=[{"host": host, "port": port, "scheme": scheme}],
        request_timeout=30,
        max_retries=3,
        retry_on_timeout=True,
    )
    return _client


def reset_client() -> None:
    """Reset the singleton client (useful for testing or reconfiguration)."""
    global _client
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
    _client = None


def ping(client: Optional[Elasticsearch] = None) -> bool:
    """Check if Elasticsearch is reachable.

    Args:
        client: ES client to use. If None, uses the singleton.

    Returns:
        True if ES responded to a ping, False otherwise.
    """
    if client is None:
        client = get_client()
    try:
        return client.ping()
    except Exception:
        return False


def get_index_name(index_key: str, settings: Optional[dict] = None) -> str:
    """Resolve a logical index key to the actual ES index name.

    Args:
        index_key: One of 'episodes', 'sentences', 'vocabulary', 'expressions'.
        settings: Full settings dict. If None, loads from default path.

    Returns:
        The index name string (e.g., 'abc-episodes').

    Raises:
        KeyError: If the index_key is not defined in settings.
    """
    es_conf = get_es_config(settings)
    indices = es_conf.get("indices", {})
    if index_key not in indices:
        raise KeyError(
            f"Unknown index key '{index_key}'. " f"Available: {list(indices.keys())}"
        )
    return indices[index_key]
