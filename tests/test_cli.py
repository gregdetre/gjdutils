from typer.testing import CliRunner
from gjdutils.cli.main import app
from gjdutils.__version__ import __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "GJDutils CLI" in result.stdout
    assert "version" in result.stdout
    assert "git-clean" in result.stdout
