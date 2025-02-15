from gjdutils.functions import variable_from_caller


def vprint(min_verbosity: int, msg: str, /, **kwargs):
    """Print if the caller's verbosity level is >= min_verbosity, e.g.

        verbose = 2
        vprint(1, "Hello, world!")  # prints because verbose >= 1

    This function looks for a `verbose` variable in the caller's scope.

    Args:
        min_verbosity: Minimum verbosity level required to print (positional-only)
        **kwargs: Arguments to pass to print()

    Raises:
        ValueError: If 'verbose' variable is not found in caller's scope
    """
    # get the `verbose` variable from the caller context
    verbose = variable_from_caller("verbose")

    if verbose >= min_verbosity:
        print(msg, **kwargs)
