#!/usr/bin/env python3

from rich.console import Console

from .check_locally import main as check_locally_main
from .deploy_pypitest import main as deploy_pypitest_main
from .deploy_pypiprod import main as deploy_pypiprod_main

console = Console()


def main():
    console.rule("[yellow]Starting Full Deployment Process")

    check_locally_main()
    deploy_pypitest_main()
    deploy_pypiprod_main()

    console.print("\n[green]Full deployment process completed successfully! 🎉[/green]")


if __name__ == "__main__":
    main()
