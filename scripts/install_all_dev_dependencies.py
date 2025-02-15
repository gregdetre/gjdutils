#!/usr/bin/env python3

from gjdutils.cmd import run_cmd

if __name__ == "__main__":
    run_cmd("pip install -e '.[all_no_dev,dev]'", verbose=4)
