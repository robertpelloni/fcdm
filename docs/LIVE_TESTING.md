# FCDM v16.0.0 Live Deployment Protocols

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

## 3. Hardware Diagnostics & Stress Testing
- [ ] **Industrial Stress Test**: Run `python3 scripts/industrial_stress_test.py --duration 60`.
- [ ] **Benchmark**: Jitter variance < 5ms for 99.9% of samples.
- [ ] **ML Latency**: Lookahead decoder must average < 10ms per window.
- [ ] **Calibration Drift**: Run `scripts/calibrate_fsr.py --mode DRIFT` before and after each session.

## Benchmarks
| Metric | Target | Pass/Fail |
|--------|--------|-----------|
| Boot to Wheel | < 10s | |
| Input Lag | < 15ms | |
| Crash-free Play | 2+ Hours | |
| ML Flow Efficiency| > 85% | |
