#!/bin/bash
# Fetch git submodule dependencies for FCDM
# These are tracked as gitlinks (commit references) but not as .gitmodules entries
# to prevent Jules clone --recursive from entering them and hitting stale proxy caches.
#
# Usage: ./fetch-submodules.sh [--depth 1]

DEPTH=""
if [ "$1" = "--depth" ] && [ -n "$2" ]; then
  DEPTH="--depth $2"
elif [ "$1" = "--shallow" ]; then
  DEPTH="--depth 1"
fi

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Fetching FCDM submodule dependencies into $SCRIPT_DIR"

# bobmania
if [ ! -d "$SCRIPT_DIR/bobmania" ]; then
  echo "  Cloning bobmania..."
  git clone $DEPTH https://github.com/robertpelloni/bobmania "$SCRIPT_DIR/bobmania"
  cd "$SCRIPT_DIR/bobmania"
  git checkout a44c21beee96e2cb1169eac81e3e2295daf01deb 2>/dev/null || true
  cd "$SCRIPT_DIR"
  # Fetch bobmania's own submodules (Themes, bobcoin only - extern deps removed)
  cd "$SCRIPT_DIR/bobmania"
  git submodule update --init --recursive 2>/dev/null || true
  cd "$SCRIPT_DIR"
else
  echo "  SKIP bobmania (already exists)"
fi

# itgmania
if [ ! -d "$SCRIPT_DIR/itgmania" ]; then
  echo "  Cloning itgmania..."
  git clone $DEPTH https://github.com/robertpelloni/itgmania "$SCRIPT_DIR/itgmania"
  cd "$SCRIPT_DIR/itgmania"
  git checkout 93bcd8ded6f91884884671d91c4a2e83870027d3 2>/dev/null || true
  cd "$SCRIPT_DIR"
  # Fetch itgmania's submodules (Themes, bobcoin only)
  cd "$SCRIPT_DIR/itgmania"
  git submodule update --init --recursive 2>/dev/null || true
  cd "$SCRIPT_DIR"
  # Fetch extern build deps
  if [ -f "$SCRIPT_DIR/itgmania/fetch-extern-deps.sh" ]; then
    echo "  Fetching itgmania extern build deps..."
    cd "$SCRIPT_DIR/itgmania"
    bash fetch-extern-deps.sh --shallow 2>/dev/null || true
    cd "$SCRIPT_DIR"
  fi
else
  echo "  SKIP itgmania (already exists)"
fi

echo "Done."
