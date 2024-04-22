import inspect
import sys
import traceback


def str_from_exception(name=None):
    return {
        "name": name,
        "msg": "".join(traceback.format_exception(*sys.exc_info())),
    }


def func_name():
    # https://stackoverflow.com/a/13514318/230523
    return inspect.currentframe().f_back.f_code.co_name
