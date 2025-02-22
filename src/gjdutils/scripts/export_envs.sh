#!/bin/bash

# https://stackoverflow.com/a/20909045/230523
# e.g. source scripts/export_envs.sh .env && echo $TESTME

# this can't be a Python script, because the whole point is to
# add environment variables to the current shell, and Unix won't
# let a script manipulate its parent environment.
# 
# see pyproject.toml for how `install.py` automatically gets called
# by `pip install`

# Check if the script is being sourced
if [ "$0" = "$BASH_SOURCE" ]; then
    echo "Error: This script needs to be sourced. Please run: source $0 <env-file>"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "Error: Environment file path is required"
    echo "Usage: source $0 <env-file>"
    return 1
fi

ENV_FILE="$1"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: File '$ENV_FILE' does not exist"
    return 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)