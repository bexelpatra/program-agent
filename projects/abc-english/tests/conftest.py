"""Shared test configuration.

Installs mock modules for third-party packages that may not be available
in the test environment (e.g. spacy).
"""

import sys
from types import ModuleType
from unittest.mock import MagicMock


def _install_mock_spacy():
    """Install a fake ``spacy`` package into sys.modules if the real one is missing."""
    if "spacy" in sys.modules:
        return  # real spacy is available — nothing to do

    try:
        import spacy  # noqa: F401

        return  # real spacy importable — nothing to do
    except ImportError:
        pass

    # Create mock spacy module hierarchy
    mock_spacy = MagicMock(spec=ModuleType)
    mock_spacy.__name__ = "spacy"
    mock_spacy.__package__ = "spacy"

    mock_language = MagicMock(spec=ModuleType)
    mock_language.__name__ = "spacy.language"
    mock_language.__package__ = "spacy"
    # Provide a Language class (just a plain class for type annotations)
    mock_language.Language = type("Language", (), {})
    mock_spacy.language = mock_language
    mock_spacy.Language = mock_language.Language  # shortcut used by some code

    sys.modules["spacy"] = mock_spacy
    sys.modules["spacy.language"] = mock_language


# Run at import time so that ``import spacy`` in src.analyzer succeeds
# during test collection.
_install_mock_spacy()
