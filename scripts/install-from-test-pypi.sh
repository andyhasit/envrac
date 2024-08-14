#!/bin/bash
set -euo pipefail

# TODO check we're not in envrac?
pip uninstall envrac && python -m pip install -i https://test.pypi.org/simple envrac