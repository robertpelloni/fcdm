#!/bin/bash
# FCDM v24.1.0 Industrial Build Script
# Compiles the customized ITGMania engine.

cd itgmania
cmake -B Build -G "Unix Makefiles"
cmake --build Build --parallel $(nproc)
echo "Build Complete."
