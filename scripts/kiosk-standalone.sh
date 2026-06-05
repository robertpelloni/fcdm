#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Optimize for audio latency (ALSA)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
export SDL_AUDIODRIVER=alsa
export ALSA_CARD=0

# 3. Disable screen blanking
xset s off
xset -dpms
xset s noblank

# 4. Launch ITGMania in the custom theme
cd itgmania
./itgmania --theme FitnessKiosk --kiosk
