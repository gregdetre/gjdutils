# Git Commit Guidelines

## Initial Assessment
Have a look at Git diff. Batch the changes into commits, and make them one at a time.

## Commit Best Practices

### Don't ever do anything destructive

ABOVE ALL, don't do anything that could result in lost work or mess up yet-to-be-committed changes, unless EXPLICITLY instructed to by the user after warning them.


### Batching changes into commits
- Each commit should represent a small/medium feature, or stage, or cluster of related changes (e.g. tweaking a bunch of docs).
- But strike a balance, e.g. the code and docs changes for a given feature should be in the same commit.
- The codebase should (ideally) be in a working state after each commit.
- Try not to mix unrelated changes.
- Before making the commit, list all files that will be committed.
- IMPORTANT If this is being run in a conversation, only commit changes relevant to this conversation. (Still use reset/add/commit single-command chaining)
- When choosing the order of batches, prefer batches that concern files with older modification dates, in order to make it less likely that another agent is still working on them.


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
There may be other agents changing the code while you work, and they might have added other files already.
- IMPORTANT: To minimise interference, ALWAYS chain the reset/add/commit operations (to make sure we unstage first, then stage, then commit, atomically):
  ```bash
  git reset HEAD unwanted-file && git add wanted-file && git commit -m "fix: resolve auth bug"
  ```
- This reduces the window where another agent's changes could interfere

### Important Notes
- If the code is in a partial/broken state, prioritise commits that leave the codebase working
- If you encounter merge conflicts or ANY unexpected issues, stop and ask the user immediately
- When in doubt, ask the user before proceeding
- **ALWAYS quote file paths** when using git commands to avoid shell expansion issues:
  - `git add "frontend/src/routes/language/[target_language_code]/+page.svelte"`
  - This is especially important for SvelteKit routes with brackets: `[param]`


### Gitignore

If you notice files that almost certainly shouldn't be committed (e.g. `node_modules`, `passwords.secret`), read the `.gitignore`, and stop to ask the user whether to add them to it.


## Parallel AI Assistance

Run this with parallel AI subagents unless there is a good reason not to. Provide it with lots of context about what we've been doing that will help it to make good decisions and write a good commit message.