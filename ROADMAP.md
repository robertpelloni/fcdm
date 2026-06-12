# Roadmap: Fitness Center Dance Machine

## Milestone 1: Foundation & Research [DONE]
- [x] Initialize repository with submodules (BobMania, ITGMania).
- [x] Analyze StepMania/OutFox/ITGMania theme engines.

## Milestone 2: Minimalist Kiosk Theme [DONE]
- [x] Create a stripped-down Lua theme skeleton for ITGMania.
- [x] Implement 1-10 difficulty normalization logic.
- [x] Implement minimalist "Workout Summary" and "Feedback" screens.

## Milestone 3: ML Pipeline Integration [DONE]
- [x] Develop Python script for audio analysis (BPM, downbeat) using librosa.
- [x] Integrate Production ML chart generator (OnsetNet + SymNet).
- [x] Implement "Stream Sanitizer" to ensure fitness-safe patterns.

## Milestone 4: Hardware Integration [DONE]
- [x] Design/Implement Teensy/Arduino FSR controller code.
- [x] Document hardware build (frame, panel stack, wiring).
- [x] Implement Industrial Calibration Suite (Wizard, Resonance, Drift analysis).

## Milestone 5: Full System Integration [DONE]
- [x] Create standalone kiosk entry point script.
- [x] Implement systemd service for auto-start.
- [x] Final testing and calibration (v2.0.0).
