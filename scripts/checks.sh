#!/bin/bash
set -euo pipefail

# Ensure main is up to date and all changes are in our branch
git checkout main
git pull
git checkout @{-1}
git rebase main || git rebase --abort


# pre-commit run --all-files
# pytest