import typer
from gjdutils.cli import env

app = typer.Typer(
    help="GJDutils CLI - utility functions for data science, AI, and web development",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Add command groups
app.add_typer(env.app, name="env")


@app.command()
def version():
    """Show gjdutils version"""
    from gjdutils.__version__ import __version__

    typer.echo(f"{__version__}")


if __name__ == "__main__":
    app()
