@echo off
echo === FCDM BUILD ===
cd itgmania
cmake -B Build -G "Visual Studio 17 2022" -A x64
cmake --build Build --config Release
