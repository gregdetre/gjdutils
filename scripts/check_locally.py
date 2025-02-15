#!/usr/bin/env python3

from rich.console import Console
from rich.progress import track
from pathlib import Path
import shutil
import sys

from gjdutils.shell import temp_venv, run_cmd

console = Console()


def main():
    console.rule("[yellow]Starting local package testing")

    # Clean existing builds
    # Command: rm -rf dist/ build/
    console.print("\nCleaning existing builds...", style="green")
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)

    # Build package
    # Command: python -m build
    console.print("\nBuilding package...", style="green")
    run_cmd([str(sys.executable), "-m", "build"])

    venv_path = Path("/tmp/test-gjdutils")
    with temp_venv(venv_path) as python_path:
        # Install package from wheel
        # Command: pip install dist/*.whl
        console.print("\nInstalling package from local build...", style="green")
        wheel_file = next(Path("dist").glob("*.whl"))
        run_cmd([str(python_path), "-m", "pip", "install", str(wheel_file)])

        # Install dev dependencies
        # Command: pip install ".[dev]"
        console.print("\nInstalling dev dependencies...", style="green")
        run_cmd([str(python_path), "-m", "pip", "install", ".[dev]"])

        # Test import and version
        # Command: python -c "import gjdutils; print(gjdutils.__version__)"
        console.print("\nTesting basic functionality...", style="green")
        version = run_cmd(
            [str(python_path), "-c", "import gjdutils; print(gjdutils.__version__)"]
        ).stdout.strip()
        console.print(f"gjdutils version: {version}")

        # Run tests
        # Command: python -m pytest
        console.print("\nRunning test suite...", style="green")
        test_result = run_cmd([str(python_path), "-m", "pytest"])
        if test_result.returncode != 0:
            console.print("\n[red]Test suite failed![/red]")
            console.print(test_result.stdout)
            console.print(test_result.stderr)
            return

        # Test optional features
        # Command: pip install ".[feature]" for each feature
        console.print("\nTesting optional feature installations...", style="green")
        features = ["dt", "llm", "audio_lang", "html_web"]
        for feature in track(features, description="Installing features"):
            console.print(f"\nTesting feature set: {feature}", style="yellow")
            result = run_cmd(
                [str(python_path), "-m", "pip", "install", f".[{feature}]"], check=False
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

    console.print("\nLocal testing completed successfully!", style="green")


if __name__ == "__main__":
    main()
