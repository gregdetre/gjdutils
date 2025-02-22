#!/usr/bin/env python3

from rich.console import Console
from gjdutils.shell import fatal_error_msg
from gjdutils.cmd import run_cmd

console = Console()


def check_git_clean():
    """Check if git working directory is clean."""
    # Check for unstaged changes
    retcode, stdout, _ = run_cmd("git diff --quiet", check=False)
    if retcode != 0:
        _, diff_output, _ = run_cmd("git --no-pager diff --stat")
        fatal_error_msg("Unstaged changes present:\n" + diff_output)

    # Check for staged but uncommitted changes
    retcode, stdout, _ = run_cmd("git diff --cached --quiet", check=False)
    if retcode != 0:
        _, diff_output, _ = run_cmd("git --no-pager diff --cached --stat")
        fatal_error_msg("Uncommitted staged changes present:\n" + diff_output)

    # Check for untracked files
    _, untracked, _ = run_cmd("git ls-files --others --exclude-standard")
    if untracked.strip():
        fatal_error_msg(f"Untracked files present:\n{untracked}")

    console.print("[green]Git: clean[/green]")


def main():
    console.rule("[yellow]Checking Git Status")
    check_git_clean()


if __name__ == "__main__":
    main()
