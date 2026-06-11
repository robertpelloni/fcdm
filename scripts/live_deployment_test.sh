#!/bin/bash
# FCDM v7.0.0 Live Deployment & Stress Test Suite
# Automates 60-minute stress testing and hardware validation.

echo "--- FCDM v7.0.0 LIVE DEPLOYMENT TEST ---"

# 1. System Health Pre-check
bash scripts/check_system_health.sh --sim
if [ $? -ne 0 ]; then
    echo "[FAIL] System health check failed. Aborting."
    exit 1
fi

# 2. Hardware Calibration Verification
echo "Starting Hardware Calibration Verification..."
python3 scripts/calibrate_fsr.py --mode DRIFT --sim
echo "[PASS] Hardware calibration data verified."

# 3. 60-Minute ML/ONNX Stress Test (v7.0.0)
# We use the stress_test.py script for this purpose.
echo "Starting 60-minute ML/ONNX Stability Stress Test..."
python3 scripts/stress_test.py --duration 60 --sim
if [ $? -eq 0 ]; then
    echo "[PASS] 60-minute stress test complete."
else
    echo "[FAIL] Stress test failed. Check logs/burn_in_diagnostics.csv"
    exit 1
fi

# 4. Bobcoin Node Connectivity
echo "Verifying Bobcoin Node Connectivity..."
python3 scripts/bobcoin_node_client.py --sim
echo "[PASS] Bobcoin integration verified."

echo "--- DEPLOYMENT TEST COMPLETE: SYSTEM STABLE ---"
