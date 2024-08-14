#!/bin/bash
set -euo pipefail

./scripts/checks.sh
rm -rf dist
rm -rf envrac.egg-info
python -m build
