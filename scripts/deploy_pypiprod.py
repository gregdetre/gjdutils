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
from gjdutils.cmd import run_cmd
from scripts.check_git_clean import check_git_status

console = Console()


def main():
    console.rule("[yellow]Starting Production PyPI Deployment")

    # Check git status first
    check_git_status()

    # Check if version already exists
    if check_version_exists(Version(__version__), pypi_env="prod"):
        fatal_error_msg(
            f"Version {__version__} already exists on PyPI.\nPlease update __VERSION__.py to a new version number first."
        )

    # Confirm with user before proceeding
    version_confirm = input(
        f"\nAre you sure you want to deploy version {__version__} to production PyPI? (y/N): "
    )
    if version_confirm.lower() != "y":
        console.print("\n[yellow]Deployment cancelled by user[/yellow]")
        return

    # Execute deployment steps
    clean_build_dirs()
    build_package()
    upload_to_pypi(pypi_env="prod")

    console.print("\n[green]Deployment to Production PyPI completed![/green]")
    console.print("Run ./scripts/check_pypiprod.py to verify the deployment")


if __name__ == "__main__":
    main()
