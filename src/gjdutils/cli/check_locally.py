#!/usr/bin/env python3

from rich.console import Console
from pathlib import Path
import shutil

from gjdutils.decorators import console_print_doc
from gjdutils.shell import temp_venv
from gjdutils.cmd import run_cmd
from gjdutils.pypi_build import verify_installation, check_install_optional_features

console = Console()


@console_print_doc(color="yellow")
def clean_build_dirs():
    """Cleaning existing builds..."""
    # Command: rm -rf dist/ build/
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)


def build_package():
    return run_cmd(
        f"python -m build",
        before_msg="Building package...",
        fatal_msg="Failed to build package",
    )


def install_and_test_package(python_path: Path, wheel_file: Path):
    """Installing and testing package..."""
    # Command: pip install dist/*.whl
    run_cmd(
        f"{python_path} -m pip install {wheel_file}",
        before_msg="Installing package wheel file from local build...",
        fatal_msg="Failed to install package",
    )

    # Install all optional dependencies first
    check_install_optional_features(python_path)

    # Command: pip install ".[dev]"
    run_cmd(
        f"{python_path} -m pip install '.[dev]'",
        before_msg="Installing dev dependencies...",
        fatal_msg="Failed to install dev dependencies",
    )


def run_test_suite(python_path: Path):
    return run_cmd(
        f"{python_path} -m pytest",
        before_msg="Running test suite...",
        fatal_msg="Test suite failed",
    )


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

    console.print("\nLocal testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
