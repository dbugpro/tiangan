#!/usr/bin/env bash
set -euxo pipefail

# Install the tiangan Python wrapper using pip
# --no-deps ensures Conda, not pip, resolves dependencies
# --ignore-installed avoids conflicts with base environment packages
$PYTHON -m pip install . --no-deps --ignore-installed -vv

