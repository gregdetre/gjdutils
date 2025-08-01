# Automated testing

Always run tests with `pytest` (rather than `python -m blah`). Most of the time it's better to just run relevant tests, and only occasionally run all of them (e.g. after making major/wide-ranging changes).

If you've run the tests recently, use the `-x` and `--lf` flags, so that we zero in on the failing tests and avoid too much output.

Test functions should always be called `test_*.py`. Avoid creating test-related utility or fixture functions called `test_*.py` to avoid confusion with actual tests.

Write a test before writing new code. Run relevant tests after changing code.

Keep tests simple and readable. Start with testing the simple cases. Make a proposal and ask the user whether edge cases are important.

Aim to reuse fixtures and sample data.

When changing tests, make minimal changes that are directly relevant to the task at hand.

If there is a `docs/TESTING.md`, or `docs/FRONTEND_TESTING.md`, `docs/BACKEND_TESTING.md`, treat them as more important than these instructions.