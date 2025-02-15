import pytest
from gjdutils.print_utils import vprint


def test_vprint_basic():
    verbose = 2
    # Should print
    vprint(1, "test1", end="")  # Empty print
    vprint(1, "test2", sep=" ", end="\n")  # Print with kwargs
    vprint(2, "test3", end="")  # Exact match

    # Should not print
    vprint(3, "test4", end="")


def test_vprint_missing_verbose():
    # Should raise ValueError when verbose is not defined
    with pytest.raises(ValueError) as exc_info:
        vprint(0, "test", end="")
    assert "verbose" in str(exc_info.value)
    assert "not found in caller function" in str(exc_info.value)


def test_vprint_args_validation():
    verbose = 1
    # Should raise TypeError when passing extra positional args
    with pytest.raises(TypeError) as exc_info:
        vprint(1, "msg", "extra arg")  # type: ignore
    assert "positional argument" in str(exc_info.value)

    # Should raise TypeError when required positional args are missing
    with pytest.raises(TypeError) as exc_info:
        vprint(msg="A message", min_verbosity=1)  # type: ignore
    assert "missing 2 required positional arguments" in str(exc_info.value)
