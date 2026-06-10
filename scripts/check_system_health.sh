#!/bin/bash
# FCDM System Health Check (v2.8.0)
# This script automates pre-live-testing verification.

echo "--- FCDM SYSTEM HEALTH CHECK ---"

# 1. ALSA Check
if command -v aplay > /dev/null; then
    echo "[PASS] ALSA (aplay) found."
    aplay -l | grep -i "card"
else
    echo "[FAIL] ALSA utilities missing."
fi

# 2. Serial (FSR) Check
if [ -e "/dev/ttyACM0" ]; then
    echo "[PASS] FSR Controller (/dev/ttyACM0) detected."
    ls -l /dev/ttyACM0
else
    echo "[WARN] /dev/ttyACM0 not found. Check physical connection or use --sim."
fi

# 3. ML Environment
python3 -c "import onnxruntime; print('[PASS] ONNX Runtime loaded.')" 2>/dev/null || echo "[WARN] onnxruntime missing. Using fallback inference."
python3 -c "import librosa; print('[PASS] Librosa loaded.')" 2>/dev/null || echo "[FAIL] librosa missing."

echo "--------------------------------"
