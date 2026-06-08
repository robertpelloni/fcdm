# Follow-up Actions & Technical Debt

## High Priority: ML Integration
- **Task**: Deepen the DDC (Dance Dance Convolution) integration for better chart variety.
- **Status**: Transitioned from heuristic skeleton to `scripts/ddc_inference.py` which uses advanced signal processing (Mel-spectrograms and Onset detection) to mimic deep learning density.
- **Requirement**: Native TensorFlow 0.12.1 environment or a modern ONNX port of the original DDC models for true deep learning inference.

## High Priority: Live User Testing
- **Task**: Execute the protocol in `docs/LIVE_TESTING.md`.
- **Status**: Software stack is stable (v1.3.0), but requires physical hardware assembly and calibration.
- **Blocker**: Availability of the physical FSR-based platform.

## Maintenance: Hardware Calibration
- **Task**: Refine the Teensy/Arduino FSR controller code based on real-world sensor drift.
- **Status**: Initial code is documented in `docs/HARDWARE.md`.
- **Requirement**: In-person testing with varying weights and step velocities.

## Technical Debt
- **Artifacts**: Regenerate `fitness-center-dance-machine-v1.0.0.zip` to reflect the v1.3.0 changes and rename it to `v1.3.0`.
- **BPM Robustness**: Enhance `scripts/audio_processor.py` to handle multi-BPM tracks by using `librosa` beat-alignment more granularly.
- **CI Dependency**: Monitor `audioread` for updates regarding Python 3.13 deprecations to ensure CI longevity.
