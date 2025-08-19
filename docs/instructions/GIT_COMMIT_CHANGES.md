# Git Commit Guidelines

## Initial Assessment
Have a look at Git diff. Batch the changes into commits, and make them one at a time.

## Commit Best Practices

### Don't ever do anything destructive

ABOVE ALL, don't do anything that could result in lost work or mess up yet-to-be-committed changes, unless EXPLICITLY instructed to by the user after warning them.


### Batching changes into commits
- Each commit should represent a small/medium feature, or stage, or cluster of related changes (e.g. tweaking a bunch of docs).
- The codebase should (ideally) be in a working state after each commit.
- Try not to mix unrelated changes.
- Before making the commit, list all files that will be committed.

### Commit Message Format
```
<type>: <subject> (50 chars max)

<body> (optional, wrap at 72 chars)
- Include a reference to current planning doc at the top of the commit body if there is one, e.g. "Planning doc: yyMMddx_feature_name.md"
- More detailed explanation
- Bullet points for multiple changes
```

Types: feat, fix, docs, style, refactor, test, chore

### Handling Concurrent Changes
Note: there may be other agents changing the code while you work.
- To minimise interference, chain the unstage/add/commit operations:
  ```bash
  git reset HEAD unwanted-file && git add wanted-file && git commit -m "fix: resolve auth bug"
  ```
- This reduces the window where another agent's changes could interfere

### Important Notes
- If the code is in a partial/broken state, prioritise commits that leave the codebase working
- If you encounter merge conflicts or ANY unexpected issues, stop and ask the user immediately
- When in doubt, ask the user before proceeding
- When adding files with special characters (like brackets or spaces), quote the path: `git add "path/with special chars/file.txt"`


## Parallel AI Assistance

Run this with parallel AI assistance unless there is a good reason not to. Provide it with lots of context about what we've been doing that will help it to make good decisions and write a good commit message.