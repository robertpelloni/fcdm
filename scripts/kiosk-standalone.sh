#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine (v3.1.0)

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Optimize for audio latency (ALSA)
# v3.1.0 High-Performance Buffer Tuning
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
export SDL_AUDIODRIVER=alsa
export ALSA_CARD=0
export ALSA_BUFFER_SIZE=512
export ALSA_PERIOD_SIZE=128

# 3. Disable screen blanking
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# 4. Process-level priority (if run as root)
cd itgmania
nice -n -20 ./itgmania --theme FitnessKiosk --kiosk
