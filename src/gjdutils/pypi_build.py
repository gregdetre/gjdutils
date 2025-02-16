"""Shared utilities for PyPI package building and testing."""

from pathlib import Path
import urllib.request
import urllib.error
import shutil
import tomllib
from typing import Literal
from rich.console import Console
from rich.progress import track
from packaging.version import Version
from importlib.metadata import metadata

from gjdutils.cmd import run_cmd
from gjdutils import __version__

console = Console()


def verify_installation(python_path: Path):
    # Command: python -c "import gjdutils; print(gjdutils.__version__)"
    retcode, installed_version, extra = run_cmd(
        f'{python_path} -c "import gjdutils; print(gjdutils.__version__)"',
        before_msg="Verify package installation by importing and checking version...",
        fatal_msg="Failed to import gjdutils",
    )
    expected_version = __version__
    assert (
        installed_version == expected_version
    ), f"Installed version {installed_version} does not match expected version {expected_version}"
    console.print(f"gjdutils version: {installed_version}")
    return installed_version


# Type for PyPI environment
PyPIEnv = Literal["test", "prod"]


def check_install_optional_features(python_path: Path, *, from_test_pypi: bool = False):
    """Test installation of optional feature sets."""
    # Get optional dependency groups from package metadata
    pkg_metadata = metadata("gjdutils")
    # Parse the provides-extra field to get optional dependency groups
    # get_all() returns None if the field doesn't exist
    extra_features = pkg_metadata.get_all("Provides-Extra") or []
    features = [group for group in extra_features if group not in ["dev", "all_no_dev"]]

    for feature in track(features, description="Installing features"):
        console.print(f"\nTesting feature set: {feature}", style="yellow")
        if from_test_pypi:
            cmd = f"{python_path} -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils[{feature}]"
        else:
            cmd = f"{python_path} -m pip install '.[{feature}]'"
        run_cmd(
            cmd,
            before_msg=f"Installing feature set: {feature}...",
            fatal_msg=f"Failed to install {feature} feature",
        )
        console.print(f"[green]Successfully installed {feature} feature[/green]")


def check_version_exists(version: Version, pypi_env: PyPIEnv) -> bool:
    """Check if version already exists on specified PyPI environment.

    Args:
        version: Version string to check (must be valid semantic version)
        pypi_env: PyPI environment to check ("test" or "prod")

    Raises:
        TypeError: If version is not a packaging.version.Version instance
    """
    if not isinstance(version, Version):
        raise TypeError(
            f"version must be a packaging.version.Version instance, got {type(version)}"
        )

    base_url = {
        "test": "https://test.pypi.org",
        "prod": "https://pypi.org",
    }[pypi_env]
    try:
        url = f"{base_url}/pypi/gjdutils/{str(version)}/json"
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise  # Re-raise other HTTP errors


def clean_build_dirs():
    """Clean build directories (dist/ and build/)."""
    # Command: rm -rf dist/ build/
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)


def build_package():
    """Build package with python -m build."""
    return run_cmd(
        "python -m build",
        before_msg="Building package...",
        fatal_msg="Failed to build package",
    )


def upload_to_pypi(pypi_env: PyPIEnv):
    """Upload package to specified PyPI environment.

    Args:
        pypi_env: PyPI environment to upload to ("test" or "prod")
    """
    if pypi_env == "test":
        cmd = "twine upload -r testpypi dist/*"
    elif pypi_env == "prod":
        cmd = "twine upload dist/*"
    else:
        raise ValueError(f"Invalid PyPI environment: {pypi_env}")

    return run_cmd(
        cmd,
        before_msg=f"Uploading package to {pypi_env} PyPI...",
        fatal_msg=f"Failed to upload to {pypi_env} PyPI",
    )
