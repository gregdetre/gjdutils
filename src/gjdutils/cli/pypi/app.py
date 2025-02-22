"""PyPI-related CLI commands."""

import typer
from rich.console import Console

from .check import app as check_app
from .deploy import app as deploy_app

app = typer.Typer(
    help="PyPI package management commands",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Add subcommand groups to main app
app.add_typer(check_app, name="check")
app.add_typer(deploy_app, name="deploy")

console = Console()
