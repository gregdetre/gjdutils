"""Shared utilities for PyPI package building and testing."""

from pathlib import Path
import urllib.request
import urllib.error
import shutil
from rich.console import Console
from rich.progress import track

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
    assert (
        installed_version == __version__
    ), f"Installed version {installed_version} does not match expected version {__version__}"
    console.print(f"gjdutils version: {installed_version}")
    return installed_version


def check_install_optional_features(python_path: Path, *, from_test_pypi: bool = False):
    """Test installation of optional feature sets."""
    features = [
        "audio_lang",
        "dt",
        "llm",
        "html_web",
    ]

    for feature in track(features, description="Installing features"):
        console.print(f"\nTesting feature set: {feature}", style="yellow")
        if from_test_pypi:
            cmd = f"{python_path} -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils"
        else:
            cmd = f"{python_path} -m pip install '.[{feature}]'"
        run_cmd(
            cmd,
            before_msg=f"Installing feature set: {feature}...",
            fatal_msg=f"Failed to install {feature} feature",
        )
        console.print(f"[green]Successfully installed {feature} feature[/green]")


def check_version_exists(version: str) -> bool:
    """Check if version already exists on Test PyPI."""
    try:
        url = f"https://test.pypi.org/pypi/gjdutils/{version}/json"
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


def upload_to_test_pypi():
    """Upload package to Test PyPI."""
    # Command: twine upload -r testpypi dist/*
    return run_cmd(
        "twine upload -r testpypi dist/*",
        before_msg="Uploading package to Test PyPI...",
        fatal_msg="Failed to upload to Test PyPI",
    )
