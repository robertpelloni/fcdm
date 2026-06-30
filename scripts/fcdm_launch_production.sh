#!/bin/bash
# [DEPRECATED] FCDM Bash Launcher
# As of v24.1.1, the launch sequence is managed natively by the Go orchestrator.

echo "[WARNING] fcdm_launch_production.sh is deprecated. Executing Go fcdm-orchestrator directly."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

ARGS=""
if [[ "$1" == "--sim" ]]; then
    ARGS="--sim"
fi

cd "$ROOT_DIR"
exec ./fcdm-orchestrator $ARGS
