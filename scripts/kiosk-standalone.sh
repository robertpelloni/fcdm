#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine (v3.8.0)

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Source Hardware Environment
if [ -f "./scripts/set_fsr_env.sh" ]; then
    source ./scripts/set_fsr_env.sh
fi

# 3. Optimize for audio latency (ALSA)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
export SDL_AUDIODRIVER=alsa

# 3.1 Auto-Detect ALSA Card (Teensy/USB priority)
DETECTED_CARD=$(aplay -l 2>/dev/null | grep -E "Teensy|USB" | head -n 1 | cut -d' ' -f2 | tr -d ':')
export ALSA_CARD=${DETECTED_CARD:-0}
echo "FCDM: Using ALSA Hardware Card Index: $ALSA_CARD"

# 3.2 Buffer Tuning
export ALSA_BUFFER_SIZE=512
export ALSA_PERIOD_SIZE=128

# 4. Disable screen blanking
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# 5. Theme Pathing (v21.0.0)
# Ensure the FitnessKiosk theme is visible to the itgmania engine
mkdir -p itgmania/Themes
if [ ! -L "itgmania/Themes/FitnessKiosk" ]; then
    ln -s "../../themes/FitnessKiosk" "itgmania/Themes/FitnessKiosk"
fi

# 6. Process-level priority (with fallback)
cd itgmania
if nice -n -20 true 2>/dev/null; then
    nice -n -20 ./itgmania --theme FitnessKiosk --kiosk
else
    echo "WARNING: Insufficient permissions for real-time priority (nice -20)."
    ./itgmania --theme FitnessKiosk --kiosk
fi
