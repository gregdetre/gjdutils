from functools import wraps
from rich.console import Console
from typing import Callable, TypeVar, Any, cast

console = Console()

F = TypeVar("F", bound=Callable[..., Any])


def console_print_doc(color: str = "blue") -> Callable[[F], F]:
    """
    A decorator that prints the docstring of a function when it starts running.
    The entire docstring will be printed in the specified color.

    Args:
        color (str): Color for the docstring text. Defaults to "blue".

    Example:
        @console_print_doc(color="green")
        def my_function():
            "This entire docstring will be green"
            pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if func.__doc__:
                console.print(func.__doc__.strip(), style=color)
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return decorator
