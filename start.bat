@echo off
REM FCDM Industrial Production Startup (Windows)
echo === FCDM v24.0.0 STARTUP ===
bash scripts\check_system_health.sh --sim
python scripts\bobcoin_node_client.py --sim
echo Starting ITGMania...
cd itgmania && Program\itgmania.exe
cd ..
pause
