#!/bin/bash
# FCDM Industrial Production Startup (Linux)
echo "=== FCDM v24.0.0 STARTUP ==="
bash scripts/check_system_health.sh --sim
python3 scripts/bobcoin_node_client.py --sim
echo "Starting ITGMania..."
cd itgmania && ./itgmania
cd ..
