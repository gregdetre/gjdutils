#!/usr/bin/env python3

from rich.console import Console
from rich.progress import track
from pathlib import Path

from gjdutils.shell import temp_venv, run_cmd, fatal_error_msg
from gjdutils.decorators import console_print_doc

console = Console()


@console_print_doc(color="yellow")
def install_from_test_pypi(python_path: Path):
    """Installing package from Test PyPI..."""
    # Command: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils
    result = run_cmd(
        [
            str(python_path),
            "-m",
            "pip",
            "install",
            "--index-url",
            "https://test.pypi.org/simple/",
            "--extra-index-url",
            "https://pypi.org/simple/",
            "gjdutils",
        ],
        check=False,
    )
    if result.returncode != 0:
        fatal_error_msg("Failed to install package from Test PyPI", result.stderr)


@console_print_doc(color="yellow")
def verify_installation(python_path: Path):
    """Verifying package installation..."""
    # Command: python -c "import gjdutils; print(gjdutils.__version__)"
    # we need to actually use `python -c` to check the version in the temporary venv
    result = run_cmd(
        [str(python_path), "-c", "import gjdutils; print(gjdutils.__version__)"],
        check=False,
    )
    if result.returncode != 0:
        fatal_error_msg("Failed to import gjdutils", result.stderr)
    version = result.stdout.strip()
    console.print(f"gjdutils version: {version}")


@console_print_doc(color="yellow")
def test_optional_features(python_path: Path):
    """Testing optional feature installations..."""
    features = [
        "dt",
        "llm",
        "html_web",
    ]  # Excluding audio_lang as it's known to have issues
    for feature in track(features, description="Installing features"):
        console.print(f"\nTesting feature set: {feature}", style="yellow")
        result = run_cmd(
            [
                str(python_path),
                "-m",
                "pip",
                "install",
                "--index-url",
                "https://test.pypi.org/simple/",
                "--extra-index-url",
                "https://pypi.org/simple/",
                f"gjdutils[{feature}]",
            ],
            check=False,
        )
        if result.returncode != 0:
            fatal_error_msg(f"Failed to install {feature} feature", result.stderr)
        console.print(f"[green]Successfully installed {feature} feature[/green]")


def main():
    console.rule("[yellow]Starting Test PyPI package testing")

    venv_path = Path("/tmp/test-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        install_from_test_pypi(python_path)
        verify_installation(python_path)
        test_optional_features(python_path)

    console.print("\nTest PyPI testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
