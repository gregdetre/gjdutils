import inspect
import sys
import traceback

# see also functions.func_name()


def str_from_exception(name=None):
    return {
        "name": name,
        "msg": "".join(traceback.format_exception(*sys.exc_info())),
    }
