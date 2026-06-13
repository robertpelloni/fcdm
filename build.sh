#!/bin/bash
# FCDM Industrial Build Script (Linux)
echo "=== FCDM v24.0.0 BUILD ==="
cd itgmania
cmake -B Build -G "Unix Makefiles"
cmake --build Build --parallel $(nproc)
cd ..
echo "Build Complete."
