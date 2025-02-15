#!/usr/bin/env python3

import build
from rich.console import Console
from rich.progress import track
from pathlib import Path
import glob
import json
import shutil
import sys
import twine
import urllib.request
import urllib.error

from gjdutils import __version__
from gjdutils.shell import run_cmd, fatal_error_msg
from gjdutils.decorators import console_print_doc

console = Console()


@console_print_doc(color="yellow")
def check_version_exists(version: str) -> bool:
    """Checking if version already exists on Test PyPI..."""
    try:
        url = f"https://test.pypi.org/pypi/gjdutils/{version}/json"
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise  # Re-raise other HTTP errors


@console_print_doc(color="yellow")
def clean_build_dirs():
    """Cleaning build directories (dist/ and build/)..."""
    # i.e. rm -rf dist/ build/
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)


@console_print_doc(color="yellow")
def build_package():
    """Building package with python -m build..."""
    result = run_cmd([sys.executable, "-m", "build"], check=False)
    if result.returncode != 0:
        fatal_error_msg("Failed to build package", result.stderr)


@console_print_doc(color="yellow")
def upload_to_test_pypi():
    """Uploading package to Test PyPI..."""
    dist_files = glob.glob("dist/*")
    if not dist_files:
        fatal_error_msg("No distribution files found in dist/ directory")

    result = run_cmd(["twine", "upload", "-r", "testpypi"] + dist_files, check=False)
    if result.returncode != 0:
        fatal_error_msg("Failed to upload to Test PyPI", result.stderr)


def main():
    console.rule("[yellow]Starting Test PyPI Deployment")

    # Check if version already exists
    if check_version_exists(__version__):
        fatal_error_msg(
            f"Version {__version__} already exists on Test PyPI.\nPlease update __VERSION__.py to a new version number first."
        )

    # Execute deployment steps
    clean_build_dirs()
    build_package()
    upload_to_test_pypi()

    console.print("\n[green]Deployment to Test PyPI completed![/green]")
    console.print("Run ./scripts/check_pypi_test.py to verify the deployment")


if __name__ == "__main__":
    main()
