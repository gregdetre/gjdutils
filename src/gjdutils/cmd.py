from rich.console import Console
import subprocess
import sys
import time
from typing import Union, Optional, Dict
from pathlib import Path

from gjdutils.shell import fatal_error_msg


def run_cmd(
    cmd: Union[str, list[str]],
    before_msg: Optional[str] = None,
    fatal_msg: Optional[str] = None,
    verbose: int = 2,
    replace_sys_python_executable: bool = True,
    dry_run: bool = False,
    **subprocess_kwargs,
) -> tuple[int, str, Dict]:
    """Run a shell command with enhanced output and error handling.

    Args:
        cmd: Command to run as string (shell=True) or list of strings (shell=False)
        before_msg: Optional message to display before running command (green)
        fatal_msg: Optional message to use if command fails (calls fatal_error_msg)
        verbose: Output verbosity level:
            0 = silent
            1 = show before_msg if provided
            2 = also show command being run (default)
            3 = also show working directory and duration
            4 = also show command stdout output
        replace_sys_python_executable: Replace 'python ' with sys.executable
        dry_run: If True, only print what would be run
        **subprocess_kwargs: Additional arguments passed to subprocess.run

    Returns:
        Tuple of (returncode, stdout, extra) where extra is a dict containing:
        - stderr: Standard error output
        - duration: Time taken to run command
        - cmd_str: Final command string that was run
        - cwd: Working directory
        - input_args: Original function arguments
        - subprocess_result: Full subprocess.CompletedProcess object

    Examples:
        Simple usage with string command:
        >>> retcode, out, _ = run_cmd4("ls -l", before_msg="Listing files...")
        Listing files...
        $ ls -l
        >>> print(out)
        total 8
        -rw-r--r-- 1 user user 2048 Mar 15 10:00 example.txt

        Complex usage with list command and error handling:
        >>> cmd = ["pytest", "tests/", "-v", "--cov"]
        >>> retcode, out, extra = run_cmd4(
        ...     cmd,
        ...     before_msg="Running tests with coverage...",
        ...     fatal_msg="Tests failed!",
        ...     verbose=2,
        ...     timeout=300,
        ...     check=True
        ... )
        Running tests with coverage...
        $ pytest tests/ -v --cov
        === test session starts ===
        ...
    """
    input_args = locals()

    console = Console()

    start_time = time.time()

    # Convert list command to string if needed
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd

    # Replace python executable if requested
    if replace_sys_python_executable and cmd_str.startswith("python "):
        cmd_str = f"{sys.executable} {cmd_str[7:]}"

    # Handle verbosity
    if verbose >= 1 and before_msg:
        console.print(f"[green]{before_msg}[/green]")
    if verbose >= 2:
        console.print(f"[white]$ {cmd_str}[/white]")

    # Handle dry run
    if dry_run:
        return (
            0,
            "",
            {
                "stderr": "",
                "duration": 0,
                "cmd_str": cmd_str,
                "cwd": str(Path.cwd()),
                "input_args": input_args,
                "subprocess_result": None,
            },
        )

    # Set defaults for subprocess
    subprocess_kwargs.setdefault("shell", isinstance(cmd, str))
    subprocess_kwargs.setdefault("capture_output", True)
    subprocess_kwargs.setdefault("text", True)

    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd_str,
            **subprocess_kwargs,
        )
    except subprocess.TimeoutExpired as e:
        if fatal_msg:
            fatal_error_msg(
                fatal_msg,
                f"Command timed out after {subprocess_kwargs.get('timeout', '?')}s",
            )
        raise

    duration = time.time() - start_time

    # Show additional info at verbose level 3
    if verbose >= 3:
        console.print(f"[blue]Working directory: {Path.cwd()}[/blue]")
        console.print(f"[blue]Duration: {duration:.2f}s[/blue]")
    if verbose >= 4:
        console.print(f"[blue]Command output:[/blue]\n{result.stdout}")

    # Handle errors
    if result.returncode != 0:
        # Show both stdout and stderr for failed commands
        if result.stdout:
            console.print(f"[red]Command output:[/red]\n{result.stdout}")
        if result.stderr:
            console.print(f"[red]Command error output:[/red]\n{result.stderr}")
        if fatal_msg:
            fatal_error_msg(fatal_msg)

    extra = {
        "stderr": result.stderr,
        "duration": duration,
        "cmd_str": cmd_str,
        "cwd": str(Path.cwd()),
        "input_args": input_args,
        "subprocess_result": result,
    }

    return result.returncode, result.stdout.strip(), extra
