@echo off
REM FCDM Industrial Build Script (Windows)
echo === FCDM v24.0.0 BUILD ===
cd itgmania
cmake -B Build -G "Visual Studio 17 2022" -A x64
cmake --build Build --config Release
cd ..
echo Build Complete.
pause
