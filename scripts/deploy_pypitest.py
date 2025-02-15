#!/usr/bin/env python3

from rich.console import Console
from pathlib import Path
from packaging.version import Version

from gjdutils import __version__
from gjdutils.decorators import console_print_doc
from gjdutils.pypi_build import (
    check_version_exists,
    clean_build_dirs,
    build_package,
    upload_to_pypi,
)
from gjdutils.shell import fatal_error_msg

console = Console()


def main():
    console.rule("[yellow]Starting Test PyPI Deployment")

    # Check if version already exists
    if check_version_exists(Version(__version__), pypi_env="test"):
        fatal_error_msg(
            f"Version {__version__} already exists on Test PyPI.\nPlease update __VERSION__.py to a new version number first."
        )

    # Execute deployment steps
    clean_build_dirs()
    build_package()
    upload_to_pypi(pypi_env="test")

    console.print("\n[green]Deployment to Test PyPI completed![/green]")
    console.print("Run ./scripts/check_pypitest.py to verify the deployment")


if __name__ == "__main__":
    main()
