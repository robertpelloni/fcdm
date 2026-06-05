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

## 2. Functional Flow Test
- [ ] **Instant Boot**: Does the machine bypass the title screen and load the Music Wheel within 5 seconds of engine start?
- [ ] **Difficulty Normalization**: Do the 1-10 levels match the user's perceived exertion?
- [ ] **Sanitization**: Does the chart flow feel "aerobic" (no awkward jacks or hand clusters)?
- [ ] **Workout Summary**: Is the post-game summary clear and relevant?

## 3. Feedback Loop Verification
- [ ] **Pad Input**: Does the `ScreenFeedback` correctly record Left/Start/Right panel strikes?
- [ ] **Logging**: Check `logs/Trace.log` for correct feedback strings.

## Benchmarks
| Metric | Target | Pass/Fail |
|--------|--------|-----------|
| Boot to Wheel | < 10s | |
| Input Lag | < 15ms | |
| Crash-free Play | 2+ Hours | |
