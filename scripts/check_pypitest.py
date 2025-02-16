#!/usr/bin/env python3

from rich.console import Console
from pathlib import Path

from gjdutils.decorators import console_print_doc
from gjdutils.shell import temp_venv
from gjdutils.cmd import run_cmd
from gjdutils.pypi_build import verify_installation, check_install_optional_features

console = Console()


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


def main():
    console.rule("[yellow]Starting Test PyPI package testing")

    venv_path = Path("/tmp/test-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        install_from_test_pypi(python_path)
        verify_installation(python_path)

    console.print("\nTest PyPI testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
