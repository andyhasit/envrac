#!/bin/bash
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
VERSION=$(python -c 'import envrac; print(envrac.__version__)')
echo "Branch: $BRANCH"
echo "Version: $VERSION"

if [[ "$BRANCH" != "main" ]]; then
    echo You may only publish to live from main
    exit 1
fi

./scripts/build.sh
python -m twine upload --repository pypi dist/*

git tag -a $VERSION-m "version $VERSION"
git push --tags