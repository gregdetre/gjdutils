# Shell Script Guidelines

## General Principles

- Keep things simple and readable
- Prefer Python scripts over shell scripts
- Keep scripts minimal, concise, and focused on a single task
- Break long main functions into sub-functions to make it easy to follow the logic
- Prefer to show the full tracebacks & error messages, to give the user full information. Minimise try/except. 
- Fail explicitly and loudly, e.g. , and use `set -e` in bash scripts to exit on error

## Coding details
- Scripts live in `scripts/`
- Make scripts executable with `chmod +x`
- Use `#!/bin/bash` or `#!/usr/bin/env python3` shebang lines
- Use python `Typer` if command-line arguments are needed
- Use `cmd.py` functionality, e.g. `run_cmd()`
- If there is overlapping functionality, maybe move it into `src/shell.py` or somewhere else reusable
- Use colors for better readability (green for success, yellow for warnings, red for errors)
- Show progress for long-running operations
- If it will make it easier to see what the Python is doing in a script, include a comment showing the equivalent shell commands, e.g.:
```python
# i.e. rm -rf dist/
shutil.rmtree("dist", ignore_errors=True)
```


## Examples

See `scripts/check_locally.py` for an example following most of these guidelines.
