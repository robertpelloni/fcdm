#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Ingest/Sanitize new music
echo "Starting music ingestion pipeline..."
PYTHONPATH=. python3 scripts/ingest_music.py

# 3. Optimize for audio latency (ALSA)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
export SDL_AUDIODRIVER=alsa
export ALSA_CARD=0
export ALSA_PERIOD_SIZE=128
export ALSA_BUFFER_SIZE=512

# 4. Disable screen blanking
xset s off
xset -dpms
xset s noblank

# 5. Launch ITGMania in the custom theme with high priority
cd itgmania
nice -n -20 ./itgmania --theme FitnessKiosk --kiosk
