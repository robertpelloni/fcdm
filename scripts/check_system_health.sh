#!/bin/bash
# FCDM System Health Check (v3.3.0)
# This script automates pre-live-testing verification.

echo "--- FCDM SYSTEM HEALTH CHECK ---"

# 1. ALSA Check
if command -v aplay > /dev/null; then
    echo "[PASS] ALSA (aplay) found."
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
