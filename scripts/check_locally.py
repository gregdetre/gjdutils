#!/usr/bin/env python3

from rich.console import Console
from rich.progress import track
from pathlib import Path
import shutil
import sys

from gjdutils.shell import temp_venv, run_cmd, fatal_error_msg
from gjdutils.decorators import console_print_doc

console = Console()


@console_print_doc(color="yellow")
def clean_build_dirs():
    """Cleaning existing builds..."""
    # Command: rm -rf dist/ build/
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)


@console_print_doc(color="yellow")
def build_package():
    """Building package... python -m build"""
    result = run_cmd([str(sys.executable), "-m", "build"], check=False)
    if result.returncode != 0:
        fatal_error_msg("Failed to build package", result.stderr)


@console_print_doc(color="yellow")
def install_and_test_package(python_path: Path, wheel_file: Path):
    """Installing and testing package..."""
    # Command: pip install dist/*.whl
    console.print("\nInstalling package from local build...", style="green")
    result = run_cmd(
        [str(python_path), "-m", "pip", "install", str(wheel_file)], check=False
    )
    if result.returncode != 0:
        fatal_error_msg("Failed to install package", result.stderr)

    # Command: pip install ".[dev]"
    console.print("\nInstalling dev dependencies...", style="green")
    result = run_cmd([str(python_path), "-m", "pip", "install", ".[dev]"], check=False)
    if result.returncode != 0:
        fatal_error_msg("Failed to install dev dependencies", result.stderr)


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
def run_test_suite(python_path: Path):
    """Running test suite..."""
    # Command: python -m pytest
    result = run_cmd([str(python_path), "-m", "pytest"], check=False)
    if result.returncode != 0:
        fatal_error_msg("Test suite failed", result.stdout + "\n" + result.stderr)


@console_print_doc(color="yellow")
def test_optional_features(python_path: Path):
    """Testing optional feature installations..."""
    features = ["dt", "llm", "audio_lang", "html_web"]
    for feature in track(features, description="Installing features"):
        console.print(f"\nTesting feature set: {feature}", style="yellow")
        result = run_cmd(
            [str(python_path), "-m", "pip", "install", f".[{feature}]"], check=False
        )
        if result.returncode != 0:
            fatal_error_msg(f"Failed to install {feature} feature", result.stderr)
        console.print(f"[green]Successfully installed {feature} feature[/green]")


def main():
    console.rule("[yellow]Starting local package testing")

    clean_build_dirs()
    build_package()

    venv_path = Path("/tmp/test-gjdutils")
    with temp_venv(venv_path) as python_path:
        wheel_file = next(Path("dist").glob("*.whl"))
        install_and_test_package(python_path, wheel_file)
        verify_installation(python_path)
        run_test_suite(python_path)
        test_optional_features(python_path)

    console.print("\nLocal testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
