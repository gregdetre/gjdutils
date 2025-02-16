"""
GJDutils - A collection of useful utility functions
"""

from importlib.metadata import metadata, PackageNotFoundError

try:
    # Get version from package metadata (works for both installed and editable mode)
    pkg_metadata = metadata("GJDutils")  # case-sensitive!
    __version__ = pkg_metadata["Version"]
except PackageNotFoundError:
    raise RuntimeError(
        "Could not determine gjdutils version. "
        "This usually means the package is not properly installed. "
        "Please install via pip or in editable mode with 'pip install -e .'"
    )
