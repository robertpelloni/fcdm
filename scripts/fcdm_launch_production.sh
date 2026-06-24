#!/bin/bash
# FCDM v24.1.0 Production Orchestrator
# Launches the entire stack for industrial deployment sessions.

echo "--- FCDM obsidian production launch ---"

# 1. Environment Setup
source scripts/set_fsr_env.sh

# 2. Launch Bobcoin Node Watcher (Background)
echo "Starting Bobcoin Node Watcher..."
python3 scripts/bobcoin_node_client.py --watcher &
WATCHER_PID=$!

# 3. Launch Live Hardware Monitor (Background)
echo "Starting Live Hardware Monitor..."
python3 scripts/live_hardware_monitor.py --duration 120 &
MONITOR_PID=$!

# 4. Launch ITGMania
echo "Launching ITGMania Engine..."
nice -n -20 ./itgmania/itgmania --theme FitnessKiosk
# echo "  [SIM] Engine start simulated."

# 5. Cleanup on Exit
function cleanup {
    echo "Shutting down FCDM stack..."
    kill $WATCHER_PID
    kill $MONITOR_PID
}
trap cleanup EXIT

echo "FCDM Stack Active. Monitoring for 2 hours."
sleep 5
