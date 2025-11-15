# Pull/Push local `gjdutils` repos — concise prompt

Paste this prompt to rerun the workflow:

```
Find all directories named "gjdutils" under $HOME/Dropbox/dev and $HOME/dev (exclude paths containing , `.venv`, `site-packages`).

For each found directory that is a git repo:

- First, detect uncommitted changes. Print a flat list "REPOS WITH UNCOMMITTED CHANGES" (paths with $HOME abbreviated as ~), then pause for my decision. If I reply "skip" (default), skip these repos for pull/push.

- Switch ALL found repos' GitHub remotes (any remote) from HTTPS to SSH, format: git@github.com:OWNER/NAME.git. Do this even for skipped/dirty repos.

- For the remaining clean (non-skipped) repos: run git pull --ff-only --no-rebase, then git push. Do not attempt interactive auth; rely on SSH keys.

At the end, print a concise summary with three sections:
1) REPOS WITH UNCOMMITTED CHANGES
2) PULL/PUSH RESULTS (per repo)
3) SKIPPED REPOS
4) ANY OTHER NOTES, QUESTIONS OR PROBLEMS
```


