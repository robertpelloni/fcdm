# FCDM Hardware Calibration Guide

## Industrial Tuning Protocol

### 1. Zero-Load Baseline
Before steping on the platform, run `scripts/calibrate_fsr.py`. Ensure all panels are in `IDLE` state. The `RAW` value should be significantly below the `THR` (Threshold).

### 2. Threshold Adjustment
If a panel is flickering `STRIKE` while idle, increase its threshold in `config/calibration.json`.
- **Light Touch**: 350-400
- **Industrial/Heavy**: 500-600

### 3. Drift Compensation
FSR sensors may drift due to temperature or pad compression. The v2.0.0 calibrator logs these changes to `logs/calibration_history.log`. Review this log weekly to detect sensor fatigue.

### 4. Zero-Latency Verification
Ensure the Teensy/Arduino is polling at 1000Hz. Use the `integration_test.py` to verify that the software stack is processing inputs without lag.
