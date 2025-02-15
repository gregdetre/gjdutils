"""Shell and command-line utilities."""

from pathlib import Path
import shutil
import sys
import venv
from contextlib import contextmanager
from typing import Optional, Union


@contextmanager
def temp_venv(path: Union[str, Path]):
    """Create and manage a temporary virtualenv.

    Args:
        path: Path where the virtualenv should be created

    Yields:
        Path to the Python executable in the virtualenv

    Example:
        ```python
        with temp_venv("/tmp/my-venv") as python_path:
            run_cmd([python_path, "-m", "pip", "install", "some-package"])
        ```
    """
    path = Path(path)

    # Clean up any existing venv first
    if path.exists():
        shutil.rmtree(path)

    venv.create(path, with_pip=True)

    # Get the correct python executable path for this venv
    if sys.platform == "win32":
        python_path = path / "Scripts" / "python.exe"
    else:
        python_path = path / "bin" / "python"

    try:
        yield python_path
    finally:
        if path.exists():
            shutil.rmtree(path)


def fatal_error_msg(msg: str, stderr: Optional[str] = None) -> None:
    """Print a fatal error message and exit with code 1.

    Args:
        msg: The error message to display
        stderr: Optional stderr output to display after the message

    Example:
        ```python
        if result.returncode != 0:
            fatal_error_msg("Failed to build package", result.stderr)
        ```
    """
    from rich.console import Console

    console = Console()

    console.print(f"[red]{msg}[/red]")
    if stderr:
        console.print(stderr)
    sys.exit(1)
