#!/usr/bin/env bash
set -euxo pipefail

docker build -f Dockerfile.conda -t tiangan-conda .

docker run --rm \
    -v "$(pwd)":/workspace \
    tiangan-conda \
    conda build recipe --output-folder conda-dist

