# Git Commit Guidelines

## Initial Assessment
Have a look at Git diff. Think about how to batch the changes into commits:
- If you have been instructed to make the commits, then do so, one at a time.
- If not, then just suggest what the batches would be.

## Commit Best Practices

### Batching changes into commits
- Each commit should represent a small/medium feature, or stage, or cluster of related changes (e.g. tweaking a bunch of docs).
- The codebase should (ideally) be in a working state after each commit
- Try not to mix unrelated changes

### Commit Message Format
```
<type>: <subject> (50 chars max)

<body> (optional, wrap at 72 chars)
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
- When adding files with special characters (like `[slug]`), quote the path: `git add "app/documents/[slug]/page.tsx"`
- Use a subagent where appropriate