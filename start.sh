#!/bin/bash
# FCDM v24.1.0 Production Startup
# Orchestrates the industrial FCDM stack initialization.

# 1. Hardware & Environment Setup
source scripts/set_alsa_card.sh 2>/dev/null
source scripts/set_fsr_env.sh 2>/dev/null

# 2. Launch Bobcoin Node Watcher (Background)
python3 scripts/bobcoin_node_client.py --watcher &
WATCHER_PID=$!

# 3. Launch ITGMania Engine
cd itgmania && nice -n -20 ./itgmania --theme FitnessKiosk

# 4. Cleanup
kill $WATCHER_PID
