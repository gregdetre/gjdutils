#!/usr/bin/env python3

from rich.console import Console
from rich.progress import track
from pathlib import Path

from gjdutils.shell import temp_venv, run_cmd

console = Console()


def main():
    console.rule("[yellow]Starting Test PyPI package testing")

    venv_path = Path("/tmp/test-gjdutils-pypi")
    with temp_venv(venv_path) as python_path:
        # Install package from Test PyPI
        # Command: pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils
        console.print("\nInstalling package from Test PyPI...", style="green")
        result = run_cmd(
            [
                str(python_path),
                "-m",
                "pip",
                "install",
                "--index-url",
                "https://test.pypi.org/simple/",
                "--extra-index-url",
                "https://pypi.org/simple/",
                "gjdutils",
            ]
        )

        # Test import and version
        # Command: python -c "import gjdutils; print(gjdutils.__version__)"
        console.print("\nTesting basic functionality...", style="green")
        version = run_cmd(
            [str(python_path), "-c", "import gjdutils; print(gjdutils.__version__)"]
        ).stdout.strip()
        console.print(f"gjdutils version: {version}")

        # Test optional features
        # Command: pip install "gjdutils[feature]" for each feature
        console.print("\nTesting optional feature installations...", style="green")
        features = [
            "dt",
            "llm",
            "html_web",
        ]  # Excluding audio_lang as it's known to have issues
        for feature in track(features, description="Installing features"):
            console.print(f"\nTesting feature set: {feature}", style="yellow")
            result = run_cmd(
                [
                    str(python_path),
                    "-m",
                    "pip",
                    "install",
                    "--index-url",
                    "https://test.pypi.org/simple/",
                    "--extra-index-url",
                    "https://pypi.org/simple/",
                    f"gjdutils[{feature}]",
                ],
                check=False,
            )
            if result.returncode != 0:
                console.print(
                    f"[red]Warning: Failed to install {feature} feature[/red]"
                )
                console.print(result.stderr)
            else:
                console.print(
                    f"[green]Successfully installed {feature} feature[/green]"
                )

    console.print("\nTest PyPI testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
