# Roadmap: Fitness Center Dance Machine

## Milestone 1: Foundation & Research [DONE]
- [x] Initialize repository with submodules (BobMania, ITGMania).
- [x] Analyze StepMania/OutFox/ITGMania theme engines.

## Milestone 2: Minimalist Kiosk Theme [DONE]
- [x] Create a stripped-down Lua theme skeleton for ITGMania.
- [x] Implement 1-10 difficulty normalization logic.
- [x] Wire 1-10 normalization to the Music Wheel UI.
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
- [x] Final testing and calibration (v24.1.0).

### v24.1.0 Industrial Onyx Stable [DONE]
- [x] Coordinate-Aware Kinematic Viterbi Decoder (8-step lookahead).
- [x] Elite Tournament-Grade Pattern Vocabulary.
- [x] ALSA Multi-Card prioritizaton and auto-discovery.
- [x] Bobcoin Node Client robust pathing and Flow-Bonus reward logic.
- [x] Unified management protocol via run_pipeline.py.
- [x] Integrated v24.1.0 Coordinate-Aware decoder for elite ergonomics.

## Milestone 6: Clean-room Go Rewrite [IN PROGRESS]
- [x] Draft implementation phasing plan (`docs/GO_REWRITE_PLAN.md`).
- [x] Initialize Go orchestration skeleton (`src/go-orchestrator/main.go`).
- [ ] Phase 1: Migrate bash hardware/environment management to Go.
- [ ] Phase 2: Migrate Python pipeline orchestration (`run_pipeline.py`).
- [ ] Phase 3: Implement internal HTTP server for remote Kiosk management.
- [ ] Phase 4: Bind ONNX runtime to Go and deprecate Python ML inference.
