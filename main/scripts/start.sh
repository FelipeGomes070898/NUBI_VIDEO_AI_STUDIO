#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m uvicorn backend.main:app --host "${NUBI_HOST:-127.0.0.1}" --port "${NUBI_PORT:-8000}"
