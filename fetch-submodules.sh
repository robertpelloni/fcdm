#!/bin/bash
# fetch-submodules.sh - FCDM Submodule Synchronization Protocol
# Usage: bash fetch-submodules.sh [--shallow]

SHALLOW=""
if [ "$1" == "--shallow" ]; then
    SHALLOW="--depth 1"
fi

echo "Initializing and updating submodules recursively..."
git submodule update --init --recursive $SHALLOW

# Ensure bobmania and itgmania are tracking their respective branches
echo "Syncing submodules to latest tracked commits..."
git submodule foreach --recursive 'git fetch --all && git checkout $(git config -f $top_level/.gitmodules submodule.$name.branch || echo main)'

echo "FCDM Submodule Sync Complete."
