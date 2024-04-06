#!/bin/bash

set -ex

prev_dir=$(pwd)
cd "$(dirname "$0")"

python extract-openapi.py
cp openapi.yaml client/openapi.yaml
cd client && yarn codegen && cd ..

cd "$prev_dir"