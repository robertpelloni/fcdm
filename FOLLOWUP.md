# Follow-up Actions & Technical Debt

## High Priority: Live User Testing
- **Task**: Execute the protocol in `docs/LIVE_TESTING.md`.
- **Status**: Software stack is verified stable (v1.8.0), now ready for physical assembly.
- **Blocker**: Availability of the physical FSR-based platform.

## Maintenance: Hardware Calibration
- **Task**: Refine the Teensy/Arduino FSR controller code based on real-world sensor drift.
- **Status**: Initial code and interactive calibration utility (`scripts/calibrate_fsr.py`) are documented.
- **Requirement**: In-person testing with varying weights and step velocities.

## Technical Debt
- **Artifacts**: Release zip regenerated for v1.8.0.
- **ML Refinement**: True native deep learning inference via ONNX porting of DDC weights (currently using advanced Mel-spectrogram signal processing heuristics).
- **CI Dependency**: Monitor `audioread` for updates regarding Python 3.13 deprecations.
