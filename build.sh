#!/bin/bash
# FCDM v24.1.0 Build Script (Linux)
cd itgmania
cmake -B Build -G "Unix Makefiles"
cmake --build Build --parallel $(nproc)
