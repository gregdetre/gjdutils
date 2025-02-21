from pathlib import Path
import typer
from gjdutils.env import get_env_var

app = typer.Typer(
    help="Environment variable management commands",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def export(
    env_file: Path = typer.Argument(
        ...,  # Makes it required
        help="Path to .env file",
        exists=True,
    )
):
    """Export environment variables from file to shell"""
    # This is just a placeholder - we'll implement the actual functionality later
    typer.echo(f"Exporting variables from {env_file}")
    try:
        # Just test that we can read an env var
        test_var = get_env_var("PATH")
        typer.echo(f"Successfully read PATH={test_var[:20]}...")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
