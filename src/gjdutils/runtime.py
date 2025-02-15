import sys

from gjdutils.env import get_env_var
from gjdutils.pytest_utils import in_pytest


def in_notebook() -> bool:
    # from https://stackoverflow.com/q/15411967
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def in_colab():
    return "google.colab" in sys.modules
