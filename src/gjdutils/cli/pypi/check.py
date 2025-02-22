#!/usr/bin/env python3

import typer
from rich.console import Console
from pathlib import Path
import shutil

from gjdutils.decorators import console_print_doc
from gjdutils.shell import temp_venv
from gjdutils.cmd import run_cmd
from gjdutils.pypi_build import verify_installation, check_install_optional_features

# Create the check subcommand group
app = typer.Typer(
    help="Check package installation",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
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


def install_and_test_locally(python_path: Path, wheel_file: Path):
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


@app.command(name="local")
def check_local():
    """Test package installation and functionality locally."""
    console.rule("[yellow]Starting local package testing")

    clean_build_dirs()
    build_package()

    venv_path = Path("/tmp/test-gjdutils")
    with temp_venv(venv_path) as python_path:
        wheel_file = next(Path("dist").glob("*.whl"))
        install_and_test_locally(python_path, wheel_file)
        verify_installation(python_path)
        run_test_suite(python_path)

    console.print("\nLocal testing completed successfully!", style="green")


def install_from_test_pypi(python_path: Path):
    # Command: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils
    run_cmd(
        f"{python_path} -m pip install --index-url https://test.pypi.org/simple/ "
        "--extra-index-url https://pypi.org/simple/ gjdutils",
        before_msg="Installing package from Test PyPI...",
        fatal_msg="Failed to install package from Test PyPI",
    )

    # Install all optional dependencies
    check_install_optional_features(python_path, from_test_pypi=True)


@app.command(name="test")
def check_test():
    """Test package installation from Test PyPI."""
    console.rule("[yellow]Starting Test PyPI package testing")

    venv_path = Path("/tmp/test-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        install_from_test_pypi(python_path)
        verify_installation(python_path)

    console.print("\nTest PyPI testing completed successfully!", style="green")


def install_from_pypiprod(python_path: Path):
    # Command: pip install gjdutils
    run_cmd(
        f"{python_path} -m pip install gjdutils",
        before_msg="Installing package from PyPI prod...",
        fatal_msg="Failed to install package from PyPI prod",
    )

    # Install all optional dependencies
    check_install_optional_features(python_path, from_test_pypi=False)


@app.command(name="prod")
def check_prod():
    """Test package installation from Production PyPI."""
    console.rule("[yellow]Starting Production PyPI package testing")

    venv_path = Path("/tmp/prod-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        install_from_pypiprod(python_path)
        verify_installation(python_path)

    console.print("\nProduction PyPI testing completed successfully!", style="green")
