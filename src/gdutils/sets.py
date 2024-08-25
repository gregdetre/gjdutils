def assert_sets_identical(set1: set, set2: set):
    # assert that the sets are the same, and print the difference if not
    if set1 != set2:
        assert not set1 - set2, f"Set 1 has extra elements: {set1 - set2}"
        assert not set2 - set1, f"Set 2 has extra elements: {set2 - set1}"
