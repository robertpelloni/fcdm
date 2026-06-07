# Follow-up Actions & Technical Debt

## High Priority: ML Integration
- **Task**: Connect `scripts/stream_sanitizer.py` to a real ML generator output (e.g., Dancing2Night or a custom Dance_Diffusion model).
- **Status**: The ingestion pipeline is ready to receive generated charts, but the generation phase itself is currently a static skeleton.
- **Requirement**: Integration with a GPU-enabled backend or a pre-generation service.

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
