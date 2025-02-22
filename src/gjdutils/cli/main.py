import typer
from .pypi import app as pypi_app

app = typer.Typer(
    help="GJDutils CLI - utility functions for data science, AI, and web development",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Add PyPI commands
app.add_typer(pypi_app, name="pypi")


@app.command()
def version():
    """Show gjdutils version"""
    from gjdutils.__version__ import __version__

    typer.echo(f"{__version__}")


if __name__ == "__main__":
    app()
