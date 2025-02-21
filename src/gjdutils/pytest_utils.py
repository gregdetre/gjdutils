import os
import sys


def in_pytest(check_modules=True, check_env=True):
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
