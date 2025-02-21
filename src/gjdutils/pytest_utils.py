import os
import sys


def in_pytest(check_modules=True, check_env=True):
    """Detect whether code is currently running within a pytest environment.

    This function uses two different methods to check if we're running in pytest:
    1. Checking if pytest is in sys.modules (if check_modules=True)
    2. Checking if PYTEST_CURRENT_TEST is in environment variables (if check_env=True)

    Args:
        check_modules (bool, optional): Whether to check sys.modules for pytest. Defaults to True.
        check_env (bool, optional): Whether to check environment variables for PYTEST_CURRENT_TEST. Defaults to True.

    Returns:
        bool: True if all enabled checks confirm we're in pytest, False if none do.

    Raises:
        AssertionError: If both check_modules and check_env are False.
        RuntimeError: If some checks are True and others False, indicating an ambiguous state.
    """
    assert check_modules or check_env, "At least one check must be performed"
    checks = []
    if check_modules:
        # https://stackoverflow.com/a/44595269/230523
        #
        # "Of course, this solution only works if the code you're trying to test does not use pytest itself.
        mod_bool = "pytest" in sys.modules
        checks.append(mod_bool)

    if check_env:
        # from https://stackoverflow.com/a/58866220/230523
        #
        # "This method works only when an actual test is being run.
        # "This detection will not work when modules are imported during pytest collection.
        env_bool = "PYTEST_CURRENT_TEST" in os.environ
        checks.append(env_bool)

    if all(checks):
        return True
    elif not any(checks):
        return False
    else:
        raise RuntimeError(
            "It's unclear whether we're in a unit test - it might be part of the pytest setup, or you might have imported pytest as part of your main codebase."
        )
