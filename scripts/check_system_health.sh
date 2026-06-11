#!/bin/bash
# FCDM System Health Check (v5.0.0)
# This script automates pre-live-testing verification and ALSA auto-discovery.

echo "--- FCDM SYSTEM HEALTH CHECK ---"

# 1. ALSA Check & Auto-Discovery
if command -v aplay > /dev/null; then
    echo "[PASS] ALSA (aplay) found."

    # Robust multi-card discovery
    echo "  [INFO] Scanning for audio hardware..."
    CARDS=$(aplay -l | grep "card")

    # Priority: 1. Teensy, 2. USB, 3. Generic
    DETECTED_CARD=$(echo "$CARDS" | grep "Teensy" | head -n 1 | cut -d' ' -f2 | tr -d ':')
    if [ -z "$DETECTED_CARD" ]; then
        DETECTED_CARD=$(echo "$CARDS" | grep "USB" | head -n 1 | cut -d' ' -f2 | tr -d ':')
    fi

    if [ -n "$DETECTED_CARD" ]; then
        echo "  [INFO] Auto-detected Hardware Card Index: $DETECTED_CARD"
    else
        echo "  [INFO] Using default Card Index: 0"
        DETECTED_CARD=0
    fi
    export FCDM_ALSA_CARD=$DETECTED_CARD

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

# 4. Bobcoin Node Connectivity
if [ -e "scripts/bobcoin_node_client.py" ]; then
    python3 scripts/bobcoin_node_client.py --sim > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "[PASS] Bobcoin Node Client functional."
    else
        echo "[WARN] Bobcoin Node Client initialization failed."
    fi
fi

# 5. Submodule Check
if [ -d "itgmania/.git" ] && [ -d "bobmania/.git" ]; then
    echo "[PASS] Submodules initialized."
else
    echo "[WARN] Submodules missing. Run fetch-submodules.sh."
fi

echo "--------------------------------"
