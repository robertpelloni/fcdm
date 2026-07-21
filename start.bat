@echo off
echo === FCDM STARTUP ===
bash scripts\check_system_health.sh --sim
python scripts\bobcoin_node_client.py --sim
cd itgmania && Program\itgmania.exe
