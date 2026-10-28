#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
printf '\nStarting Scalar project at http://localhost:8000/\nPress Ctrl+C to stop.\n\n'
python3 -m http.server 8000
