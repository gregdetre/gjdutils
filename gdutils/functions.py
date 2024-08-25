import inspect


def func_name():
    # https://stackoverflow.com/a/13514318/230523
    return inspect.currentframe().f_back.f_code.co_name
