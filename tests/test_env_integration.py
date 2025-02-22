import os
import subprocess
import tempfile
from pathlib import Path
import pytest
from typing import Generator

from gjdutils.env import get_env_var


@pytest.fixture
def temp_env_file(tmp_path):
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("GJDUTILS_TEST_STR=hello\n")
        f.write("GJDUTILS_TEST_INT=42\n")
        path = Path(f.name)
    yield path
    path.unlink()


def test_export_envs_script(temp_env_file):
    """Test that export_envs.sh behaves correctly when executed vs sourced."""
    script_path = Path("src/gjdutils/scripts/export_envs.sh")

    # Test direct execution fails
    result = subprocess.run(
        [str(script_path), str(temp_env_file)], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "needs to be sourced" in result.stdout

    # Test sourcing works and sets variables
    result = subprocess.run(
        [
            "bash",
            "-c",
            f"source {script_path} {temp_env_file} && echo $GJDUTILS_TEST_STR",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "hello" in result.stdout


def test_get_env_var():
    """Test get_env_var functionality with different types."""
    # Set test variables directly in Python's environment (we can't use
    # export_envs.sh here because it doesn't work with subprocesses)
    os.environ["GJDUTILS_TEST_STR"] = "hello"
    os.environ["GJDUTILS_TEST_INT"] = "42"

    # Test string and int validation
    assert get_env_var("GJDUTILS_TEST_STR") == "hello"
    assert get_env_var("GJDUTILS_TEST_INT", typ=int) == 42

    # Test error cases
    with pytest.raises(ValueError, match="Missing required environment variable"):
        get_env_var("NONEXISTENT")
