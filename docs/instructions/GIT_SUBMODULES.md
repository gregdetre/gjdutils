# Git Submodules – Workflow & Best Practices

This guide explains how we use git submodules (e.g., `gjdutils`) and how to avoid common pitfalls like losing commits or pointing to the wrong revision.

## Introduction

Submodules let one repository embed another at a specific commit. They are powerful but brittle if unmanaged. Treat submodules as versioned dependencies: update deliberately, pin explicitly, and document changes.

## See also

- `WRITE_EVERGREEN_DOC.md` – how to write and maintain evergreen docs
- Parent repo docs: `docs/reference/SETUP.md` and `docs/reference/MOBILE_APP_GUIDE.md` for cloning and development
- Git docs: `git submodule` (man page)

## Principles & Decisions

- Pin submodules to explicit commits (or annotated tags), not floating branches.
- Make changes in the submodule repo itself, then update the parent pointer with a clear commit message.
- Keep submodule history reachable (branches/tags) to avoid garbage collection of important commits.
- Automate init/update steps to reduce human error.

## Daily Workflow

### Clone with submodules
```bash
git clone <parent-repo>
cd <parent-repo>
git submodule update --init --recursive
```

### Pull updates safely
```bash
git pull --rebase
git submodule update --init --recursive
```

### Update a submodule to a new commit
1) In the submodule directory, ensure the desired commit exists (pull/fetch or create it):
```bash
cd path/to/submodule
git fetch --all --tags
# create changes or checkout the commit you want
```
2) Return to parent repo and record the new pointer:
```bash
cd -  # back to parent
git add path/to/submodule
git commit -m "chore: update submodule <name> to <shortsha> (<reason>)"
```

### Make changes to a submodule
- Work inside the submodule repo (ideally on a feature branch), commit, and push.
- Back in the parent repo, stage and commit the updated submodule pointer (as above).

## Merging Branches with Submodule Changes

- When you merge a branch in the parent repo, the submodule pointer from the merge result becomes the source of truth. If your branch updates `gjdutils` to commit `X`, merging into `main` will keep `X` (subject to normal merge conflict resolution if both sides moved it).
- To avoid surprises:
  - Prefer fast-forward merges for pointer updates when feasible.
  - If both branches changed the pointer, inspect which submodule commit you want and resolve accordingly.
  - After merge, run:
    ```bash
    git submodule update --init --recursive
    ```

## Preventing Lost Work

- Keep important submodule commits on a named branch or tag so they remain reachable and won’t be garbage collected.
- Avoid force-pushing history rewrites that drop commits containing needed work.
- When developing experimental features in a submodule, push the branch early (even if WIP) so objects are stored on the remote.

## CI and Automation Tips

- Ensure CI uses:
```bash
git submodule update --init --recursive
```
- Consider a post-checkout hook that updates submodules automatically:
```bash
#!/bin/sh
git submodule update --init --recursive
```
- Add scripts to bootstrap developer environments consistently.

## Troubleshooting

- Submodule shows modified/untracked unexpectedly:
  - Run `git submodule update --init --recursive`.
  - If switching branches left files behind, clean the submodule working tree or reclone.

- Pointer mismatch after merge:
  - Inspect `.gitmodules` and `git ls-tree HEAD <submodule>`.
  - Decide which submodule commit is correct, then commit the pointer explicitly.

- Commit exists locally but not in any branch (risk of GC):
  - Create a branch or tag in the submodule pointing to that commit and push it.

## Quick Checklist

- [ ] Always `update --init --recursive` after clone/checkout
- [ ] Make changes in submodule repo; commit and push there first
- [ ] Commit the parent pointer with a clear message
- [ ] Keep important submodule commits reachable (branch or tag)
- [ ] Resolve pointer conflicts consciously during merges


