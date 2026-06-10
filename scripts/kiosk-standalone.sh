#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine (v3.7.0)

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Optimize for audio latency (ALSA)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
export SDL_AUDIODRIVER=alsa

# 2.1 Auto-Detect ALSA Card (Teensy/USB priority)
DETECTED_CARD=$(aplay -l 2>/dev/null | grep -E "Teensy|USB" | head -n 1 | cut -d' ' -f2 | tr -d ':')
export ALSA_CARD=${DETECTED_CARD:-0}
echo "FCDM: Using ALSA Hardware Card Index: $ALSA_CARD"

# 2.2 Buffer Tuning
export ALSA_BUFFER_SIZE=512
export ALSA_PERIOD_SIZE=128

# 3. Disable screen blanking
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# 4. Process-level priority (if run as root)
cd itgmania
nice -n -20 ./itgmania --theme FitnessKiosk --kiosk
