#!/bin/bash
# FCDM v24.1.0 Production Startup (Linux)
bash scripts/check_system_health.sh --sim
python3 scripts/bobcoin_node_client.py --sim
echo "Starting ITGMania..."
cd itgmania && ./itgmania
