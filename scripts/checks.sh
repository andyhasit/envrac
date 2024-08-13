#!/bin/bash
set -euo pipefail

# pre-commit run --all-files
# pytest
git checkout main
git pull
git checkout @{-1}