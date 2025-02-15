"""Shared utilities for PyPI package building and testing."""

from pathlib import Path
from rich.console import Console
from rich.progress import track

from gjdutils.cmd import run_cmd
from gjdutils import __version__

console = Console()


def verify_installation(python_path: Path):
    """Verify package installation by importing and checking version."""
    # Command: python -c "import gjdutils; print(gjdutils.__version__)"
    retcode, stdout, extra = run_cmd(
        f'{python_path} -c "import gjdutils; print(gjdutils.__version__)"',
        before_msg="Verifying package installation...",
        fatal_msg="Failed to import gjdutils",
    )
    version = stdout.strip()
    assert (
        version == __version__
    ), f"Installed version {version} does not match expected version {__version__}"
    console.print(f"gjdutils version: {version}")


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
        cmd = f"{python_path} -m pip install"

        if from_test_pypi:
            cmd += " --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/"
            cmd += f" 'gjdutils[{feature}]'"
        else:
            cmd += f" '.[{feature}]'"

        run_cmd(
            cmd,
            before_msg=f"Installing feature set: {feature}...",
            fatal_msg=f"Failed to install {feature} feature",
        )
        console.print(f"[green]Successfully installed {feature} feature[/green]")
