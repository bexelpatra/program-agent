#!/usr/bin/env bash
# projects/abc-english-app/scripts/run_dev.sh
#
# Dev-time `flutter run` wrapper that wires the required compile-time
# environment into the Flutter runtime via --dart-define.
#
# Required env vars (must be exported before invocation):
#   ABC_API_BASE_URL   e.g. http://10.0.0.5:8000
#   ABC_API_TOKEN      Static Bearer token expected by /api/v1/*
#   ABC_ENV            dev | staging | prod
#
# Usage:
#   export ABC_API_BASE_URL=http://10.0.0.5:8000
#   export ABC_API_TOKEN=<secret>
#   export ABC_ENV=dev
#   bash projects/abc-english-app/scripts/run_dev.sh [extra flutter args...]

set -euo pipefail

missing=()
[[ -z "${ABC_API_BASE_URL:-}" ]] && missing+=("ABC_API_BASE_URL")
[[ -z "${ABC_API_TOKEN:-}"    ]] && missing+=("ABC_API_TOKEN")
[[ -z "${ABC_ENV:-}"          ]] && missing+=("ABC_ENV")

if (( ${#missing[@]} > 0 )); then
  echo "ERROR: missing required environment variables:" >&2
  for v in "${missing[@]}"; do
    echo "  - $v" >&2
  done
  cat >&2 <<'EOF'

Export the variables before running, e.g.:

  export ABC_API_BASE_URL=http://10.0.0.5:8000
  export ABC_API_TOKEN=<secret>
  export ABC_ENV=dev
  bash projects/abc-english-app/scripts/run_dev.sh
EOF
  exit 1
fi

FLUTTER_BIN="${FLUTTER_BIN:-/opt/flutter/bin/flutter}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "${SCRIPT_DIR}")"

cd "${PROJECT_ROOT}"

exec "${FLUTTER_BIN}" run \
  --dart-define=ABC_API_BASE_URL="${ABC_API_BASE_URL}" \
  --dart-define=ABC_API_TOKEN="${ABC_API_TOKEN}" \
  --dart-define=ABC_ENV="${ABC_ENV}" \
  "$@"
