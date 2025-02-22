import os
import shutil
import stat
from pathlib import Path
import sys
import typer


def get_script_install_path() -> Path:
    """Get the installation path for our scripts"""
    # This will typically be something like /usr/local/bin or ~/.local/bin
    if sys.prefix == sys.base_prefix:
        # System Python installation
        if os.access("/usr/local/bin", os.W_OK):
            return Path("/usr/local/bin")
        return Path(os.path.expanduser("~/.local/bin"))
    else:
        # Virtual environment
        return Path(sys.prefix) / "bin"


def install_export_envs():
    """Install the export_envs.sh script to the appropriate location"""
    try:
        # Get our package's installed location
        package_dir = Path(__file__).parent
        source_script = package_dir / "export_envs.sh"

        if not source_script.exists():
            # Try to find it in the shared data location
            source_script = Path(sys.prefix) / "bin" / "export_envs.sh"
            if not source_script.exists():
                typer.echo(f"Error: Could not find export_envs.sh script", err=True)
                raise typer.Exit(1)

        # Get the target installation directory
        install_dir = get_script_install_path()

        # Create the directory if it doesn't exist
        install_dir.mkdir(parents=True, exist_ok=True)

        # Copy the script
        target_script = install_dir / "gjdutils-export-envs"
        shutil.copy2(source_script, target_script)

        # Make it executable
        target_script.chmod(target_script.stat().st_mode | stat.S_IEXEC)

        typer.echo(f"Installed gjdutils-export-envs to {target_script}")
        typer.echo("\nTo use this script, you need to source it:")
        typer.echo("  source gjdutils-export-envs .env")

    except Exception as e:
        typer.echo(f"Error installing script: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(install_export_envs)
