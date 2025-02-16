"""
GJDutils - A collection of useful utility functions
"""

import tomllib


def get_version() -> str:
    """Get package version from pyproject.toml.

    We read directly from pyproject.toml rather than using Python's packaging machinery
    because we've had issues with the correct version being accessed in deployment/checking
    machinery that creates virtualenvs. This provides a more reliable way to access the
    true version from the source."""
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


__version__ = get_version()
