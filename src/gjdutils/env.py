import os
from pathlib import Path
from typing import Any, TypeVar, cast
from pydantic import StrictStr, TypeAdapter

from gjdutils.print_utils import vprint

T = TypeVar("T")
_processed_vars = set()


# You may find it useful to run `python -m gjdutils.scripts.export_envs .env` to first
# export all the variables in your .env file to your environment.


def get_env_var(name: str, typ: Any = StrictStr, verbose: int = 0) -> T:
    """Get environment variable with type validation, e.g.

    OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
    NUM_WORKERS = get_env_var("NUM_WORKERS", typ=int)

    Args:
        name: Name of environment variable
        type_: Pydantic type to validate against (default: StrictStr for non-empty string)

    Returns:
        The validated value with the specified type

    Raises:
        ValueError: If variable is missing or fails validation
    """
    vprint(1, f"Attempting to get environment variable: {name}")
    vprint(2, f"Current environment variables: {list(os.environ.keys())}")
    try:
        value = os.environ[name]
        _processed_vars.add(name)

        # Use TypeAdapter for validation
        adapter = TypeAdapter(typ)
        validated = adapter.validate_python(value)

        # Return validated value directly
        return cast(T, validated)
    except KeyError:
        raise ValueError(f"Missing required environment variable: {name}")
    except Exception as e:
        raise ValueError(f"Invalid value for {name}: {e}")


def list_env_example_vars(env_example_filen: Path) -> set[str]:
    """Get set of required variables from .env.example.

    Args:
        env_example_filen: Path to the .env.example file

    Returns:
        Set of environment variable names found in the file
    """
    assert env_example_filen.exists(), f"Missing env example file: {env_example_filen}"

    required_vars = set()
    with env_example_filen.open() as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            # Get variable name (everything before =)
            var_name = line.split("=")[0].strip()
            required_vars.add(var_name)

    return required_vars
