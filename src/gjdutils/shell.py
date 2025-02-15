"""Shell and command-line utilities."""

from pathlib import Path
import shutil
import subprocess
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


def run_cmd(
    cmd: list[str], python_path: Optional[Union[str, Path]] = None, check: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and check for errors.

    Args:
        cmd: Command to run as a list of strings
        python_path: Optional path to Python executable to use
        check: Whether to raise an exception on non-zero return code

    Returns:
        CompletedProcess instance with stdout and stderr

    Example:
        ```python
        result = run_cmd(["pip", "install", "some-package"])
        print(result.stdout)
        ```
    """
    if python_path:
        cmd[0] = str(python_path)
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    return result


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
