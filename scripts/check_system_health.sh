#!/bin/bash
# FCDM System Health Check (v3.7.0)
# This script automates pre-live-testing verification and ALSA auto-discovery.

echo "--- FCDM SYSTEM HEALTH CHECK ---"

# 1. ALSA Check & Auto-Discovery
if command -v aplay > /dev/null; then
    echo "[PASS] ALSA (aplay) found."

    # Discovery logic for Teensy/USB audio
    DETECTED_CARD=$(aplay -l | grep -E "Teensy|USB" | head -n 1 | cut -d' ' -f2 | tr -d ':')
    if [ -n "$DETECTED_CARD" ]; then
        echo "  [INFO] Auto-detected Hardware Card Index: $DETECTED_CARD"
    else
        echo "  [INFO] Using default Card Index: 0"
        DETECTED_CARD=0
    fi

    # Buffer Analysis
    MEM_TOTAL=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    if [ "$MEM_TOTAL" -gt 4000000 ]; then
        echo "  [INFO] High-memory system. Recommended ALSA Buffer: 512, Period: 128"
    else
        echo "  [INFO] Low-memory system. Recommended ALSA Buffer: 1024, Period: 256"
    fi
else
    echo "[FAIL] ALSA utilities missing."
fi

# 2. Serial (FSR) Check
if [ -e "/dev/ttyACM0" ]; then
    echo "[PASS] FSR Controller (/dev/ttyACM0) detected."
else
    echo "[WARN] /dev/ttyACM0 not found. Check physical connection or use --sim."
fi

# 3. ML Environment
python3 -c "import onnxruntime; print('[PASS] ONNX Runtime loaded.')" 2>/dev/null || echo "[WARN] onnxruntime missing. Using fallback inference."
python3 -c "import librosa; print('[PASS] Librosa loaded.')" 2>/dev/null || echo "[FAIL] librosa missing."

echo "--------------------------------"
