from pytest import approx, raises

from gjdutils.num import discretise


def test_discretise():
    assert discretise(0.00, increment=0.05) == approx(0.00)
    assert discretise(0.01, increment=0.05) == approx(0.00)
    assert discretise(0.06, increment=0.05) == approx(0.05)
    assert discretise(0.99, increment=0.05) == approx(0.95)
    assert discretise(1.00, increment=0.05) == approx(1.00)
    # check values outside the range
    with raises(Exception):
        discretise(5.00, increment=0.05)
    with raises(Exception):
        discretise(-1.00, increment=0.05)
    assert discretise(-1.00, increment=0.05, enforce_range=False) == approx(0.00)
    assert discretise(5.00, increment=0.05, enforce_range=False) == approx(1.00)
