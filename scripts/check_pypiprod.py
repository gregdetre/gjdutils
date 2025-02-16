#!/usr/bin/env python3

from rich.console import Console
from pathlib import Path

from gjdutils.decorators import console_print_doc
from gjdutils.shell import temp_venv
from gjdutils.cmd import run_cmd
from gjdutils.pypi_build import verify_installation, check_install_optional_features

console = Console()


def install_from_pypiprod(python_path: Path):
    # Command: pip install gjdutils
    run_cmd(
        f"{python_path} -m pip install gjdutils",
        before_msg="Installing package from PyPI...",
        fatal_msg="Failed to install package from PyPI",
    )

    # Install all optional dependencies
    check_install_optional_features(python_path, from_test_pypi=False)


def main():
    console.rule("[yellow]Starting Production PyPI package testing")

    venv_path = Path("/tmp/prod-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        install_from_pypiprod(python_path)
        verify_installation(python_path)

    console.print("\nProduction PyPI testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
