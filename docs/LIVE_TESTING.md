# Live User Testing Protocol: v0.5.0-rc1

## Test Environment
- **OS**: Linux (Ubuntu 22.04+ or Arch)
- **Engine**: ITGMania (FitnessKiosk Theme)
- **Hardware**: 9-panel FSR Platform + Teensy 4.0
- **Audio**: Direct ALSA output

## 1. Performance Verification
- [ ] **Frame Rate**: Maintain steady 60 FPS (or monitor refresh rate).
- [ ] **Input Latency**: Verify <10ms delay between panel strike and engine response.
- [ ] **Audio Sync**: Verify no drift over a 60-minute continuous set.

## 2. v2.8.0 ML Pattern Quality
- [ ] **Flow Consistency**: Does the generated chart maintain a sustainable L-R flow for 90% of the duration?
- [ ] **Ergonomics**: Are there any "deadly" patterns (cross-overs or double-steps) that break Zone 2 aerobic pacing?

## 3. Hardware Diagnostics
- [ ] **Calibration Drift**: Run `scripts/calibrate_fsr.py --stress` before and after each session. Max allowable drift in 1 hour is <10% of threshold.
- [ ] **Poll Jitter**: Verify average polling jitter is <2ms.

## Benchmarks
| Metric | Target | Pass/Fail |
|--------|--------|-----------|
| Boot to Wheel | < 10s | |
| Input Lag | < 15ms | |
| Crash-free Play | 2+ Hours | |
| ML Flow Efficiency| > 85% | |
