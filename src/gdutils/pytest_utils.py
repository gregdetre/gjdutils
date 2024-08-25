import os
import sys


def is_pytest():
    # https://stackoverflow.com/a/44595269/230523
    #
    # "Of course, this solution only works if the code you're trying to test does not use pytest itself.
    mod_bool = "pytest" in sys.modules

    # # from https://stackoverflow.com/a/58866220/230523
    # #
    # # "This method works only when an actual test is being run.
    # # "This detection will not work when modules are imported during pytest collection.
    # env_bool = "PYTEST_CURRENT_TEST" in os.environ
    # if mod_bool and env_bool:
    #     return True
    # elif not mod_bool and not env_bool:
    #     return False
    # else:
    #     raise RuntimeError(
    #         "It's unclear whether we're in a unit test - it might be part of the pytest setup, or you might have imported pytest as part of your main codebase."
    #     )
    return mod_bool
