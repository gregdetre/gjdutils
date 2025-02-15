import inspect
from typing import Any


def func_name():
    # https://stackoverflow.com/a/13514318/230523
    return inspect.currentframe().f_back.f_code.co_name  # type: ignore


def variable_from_caller(var_name: str, frame_depth: int = 1) -> Any:
    """Get a variable from the caller's frame.

    Args:
        var_name: Name of the variable to retrieve
        frame_depth: How many frames to go back (default: 1 for immediate caller)

    Raises:
        ValueError: If the variable doesn't exist in the caller's scope
    """
    frame = inspect.currentframe()
    try:
        # Go back the specified number of frames
        for _ in range(frame_depth + 1):
            if frame.f_back is None:  # type: ignore
                raise ValueError(f"Cannot go back {frame_depth} frames")
            frame = frame.f_back  # type: ignore

        if var_name not in frame.f_locals:  # type: ignore
            caller_name = frame.f_code.co_name  # type: ignore
            raise ValueError(
                f"Variable '{var_name}' not found in caller function '{caller_name}'. "
                f"Make sure to define a '{var_name}' parameter or variable."
            )

        return frame.f_locals[var_name]  # type: ignore
    finally:
        # Clean up circular references
        del frame
