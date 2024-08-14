#!/bin/bash
set -euo pipefail

./scripts/build.sh
python -m twine upload --repository testpypi dist/*
