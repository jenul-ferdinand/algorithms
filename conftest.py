"""
Pytest root conftest.

Pins the Hypothesis example database to a single absolute location at the
repo root, so .hypothesis/ never appears inside subdirectories regardless
of where pytest is invoked from.
"""

from pathlib import Path

from hypothesis import settings
from hypothesis.database import DirectoryBasedExampleDatabase

_REPO_ROOT = Path(__file__).parent
_HYPOTHESIS_DB = _REPO_ROOT / ".hypothesis" / "examples"

settings.register_profile(
    "default",
    database=DirectoryBasedExampleDatabase(str(_HYPOTHESIS_DB)),
)
settings.load_profile("default")
