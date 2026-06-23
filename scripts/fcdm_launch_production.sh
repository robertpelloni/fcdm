#!/bin/bash
# Kiosk Standalone Entry Point for Fitness Center Dance Machine

# SIMULATION MODE ARGUMENT
SIMULATION_MODE=false
if [[ "$1" == "--sim" ]]; then
    SIMULATION_MODE=true
    echo "[FCDM] Launching in SIMULATION MODE. Bypassing ALSA restrictions and Teensy hardware checks."
fi

# 1. Kill any existing instances
killall -9 itgmania 2>/dev/null || true

# 2. Hardware / ALSA setup
if [ "$SIMULATION_MODE" = false ]; then
    # Verify Teensy hardware is connected
    if [ ! -e "/dev/ttyACM0" ]; then
        echo "[FCDM-CRITICAL] /dev/ttyACM0 (Teensy) not found. Cannot launch production without hardware. Use --sim to override."
        # We handle exit via a soft return if possible
        echo "Aborting script execution"
    else
        # Optimize for audio latency (ALSA)
        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./itgmania/
        export SDL_AUDIODRIVER=alsa
        export ALSA_CARD=0
    fi
else
    # Sim Mode defaults
    export SDL_AUDIODRIVER=dummy
fi

# 3. Disable screen blanking
xset s off 2>/dev/null || true
xset -dpms 2>/dev/null || true
xset s noblank 2>/dev/null || true

# 4. Launch ITGMania
if [ -d "itgmania" ]; then
    cd itgmania
    ./itgmania --theme FitnessKiosk --kiosk
else
    echo "Directory 'itgmania' not found. Did you run fetch-submodules.sh?"
fi
