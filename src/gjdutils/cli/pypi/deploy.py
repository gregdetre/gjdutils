"""Deployment commands for PyPI packages."""

import typer
from rich.console import Console
from packaging.version import Version

from gjdutils import __version__
from gjdutils.cli.check_git_clean import check_git_clean
from gjdutils.cli.pypi.check import check_local, check_prod, check_test
from gjdutils.pypi_build import (
    build_package,
    check_version_exists,
    clean_build_dirs,
    upload_to_pypi,
)
from gjdutils.shell import fatal_error_msg

# Create the deploy subcommand group
app = typer.Typer(
    help="Deploy package to PyPI",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()


@app.command(name="test")
def deploy_test():
    """Deploy package to Test PyPI."""
    console.rule("[yellow]Starting Test PyPI Deployment")

    # Check if version already exists
    if check_version_exists(Version(__version__), pypi_env="test"):
        fatal_error_msg(f"Version {__version__} already exists on Test PyPI.\n")

    # Execute deployment steps
    clean_build_dirs()
    build_package()
    upload_to_pypi(pypi_env="test")

    console.print("\n[green]Deployment to Test PyPI completed![/green]")
    check_test()


@app.command(name="prod")
def deploy_prod():
    """Deploy package to Production PyPI."""
    console.rule("[yellow]Starting Production PyPI Deployment")

    # Check git status first
    check_git_clean()

    # Check if version already exists
    if check_version_exists(Version(__version__), pypi_env="prod"):
        fatal_error_msg(f"Version {__version__} already exists on PyPI.\n")

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
    check_prod()


@app.command(name="all")
def deploy_all():
    """Run full deployment process (local -> test -> prod)."""
    console.rule("[yellow]Starting Full Deployment Process")

    check_local()
    deploy_test()
    deploy_prod()

    console.print("\n[green]Full deployment process completed successfully! 🎉[/green]")
