from typer.testing import CliRunner
from gjdutils.cli.main import app
from gjdutils.__version__ import __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert f"gjdutils version {__version__}" in result.stdout


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "GJDutils CLI" in result.stdout
    assert "version" in result.stdout
    assert "env" in result.stdout


def test_env_help():
    result = runner.invoke(app, ["env", "--help"])
    assert result.exit_code == 0
    assert "Environment variable management commands" in result.stdout
    assert "export" in result.stdout


def test_env_export_help():
    result = runner.invoke(app, ["env", "export", "--help"])
    assert result.exit_code == 0
    assert "Path to .env file" in result.stdout
