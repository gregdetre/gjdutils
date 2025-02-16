"""
GJDutils - A collection of useful utility functions
"""

from importlib.metadata import version, PackageNotFoundError

try:
    # The package name must match the one used in pyproject.toml
    __version__ = version("GJDutils")  # case-sensitive!
except PackageNotFoundError:
    # Package is not installed
    raise RuntimeError(
        "Could not determine gjdutils version. "
        "This usually means the package is not properly installed. "
        "Please install via pip or in editable mode with 'pip install -e .'"
    )
