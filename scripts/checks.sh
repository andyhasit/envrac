#!/bin/bash
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
VERSION=$(python -c 'import envrac; print(envrac.__version__)')
echo "Branch: $BRANCH"
echo "Version: $VERSION"

if [[ "$BRANCH" != "main" ]]; then
    if [[ "$BRANCH" != "$VERSION" ]]; then
        echo "Exiting: Branch $BRANCH must be called $VERSION"
        exit 1
    fi
    # Ensure main is up to date and all changes are in our branch too.
    git checkout main
    git pull
    git checkout @{-1}
    git rebase main || git rebase --abort
fi

pre-commit run --all-files
pytest