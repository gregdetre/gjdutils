If the user hasn't provided info about what the branch will be for, stop and ask them.

Decide on a short phrase, based on the task defined by the user, as the branch name, e.g. `refactor_blah_for_foo`

Run this in a subagent (if available):
- Check that we're on the main branch (typically `main` or `master`) or another appropriate base branch - if not, double-check with the user before continuing.
- Generate date prefix using `npx tsx src/ts/cli/sequential-datetime-prefix.ts .` and prepend to the short-phrase branch-name
- Then create that as a new branch