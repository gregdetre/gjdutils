from pytest import raises
from gjdutils.rand import assert_valid_readable_rand_id


def test_check_valid_readable_rand_id():
    # Test case: Valid ID with default parameters
    id_ = "abc234"
    assert_valid_readable_rand_id(id_)

    # Test case: Valid ID with specified number of characters
    assert_valid_readable_rand_id(id_, nchars=6)

    # Test case: Invalid ID with specified number of characters
    with raises(AssertionError):
        assert_valid_readable_rand_id(id_, nchars=8)

    assert_valid_readable_rand_id(id_, valid_chars="cba4321")

    # Test case: Invalid ID with default valid characters (doesn't allow '1')
    with raises(AssertionError):
        assert_valid_readable_rand_id(id_="abc123")
    # Test case: Invalid ID with specified valid characters
    with raises(AssertionError):
        assert_valid_readable_rand_id(id_, valid_chars="xyz123")
