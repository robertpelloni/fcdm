# Roadmap: Fitness Center Dance Machine

## Milestone 1: Foundation & Research [DONE]
- [x] Initialize repository with submodules (BobMania, ITGMania).
- [x] Analyze StepMania/OutFox/ITGMania theme engines.
- [x] Research ML-based stepchart generation (Dance_Diffusion, Omnimix).

## Milestone 2: Minimalist Kiosk Theme [DONE]
- [x] Create a stripped-down Lua theme skeleton for ITGMania.
- [x] Implement instant-boot to song selection.
- [x] Implement 1-10 difficulty normalization logic.
- [x] Wire 1-10 normalization to the Music Wheel UI.
- [x] Implement minimalist "Workout Summary" and "Feedback" screens.

## Milestone 3: ML Pipeline Integration [DONE]
- [x] Develop Python script for audio analysis (BPM, downbeat) using librosa.
- [x] Integrate ML chart generator (e.g. Dancing2Night).
- [x] Implement "Stream Sanitizer" to ensure fitness-safe patterns (No hands, no jacks).

## Milestone 4: Hardware Integration [DONE]
- [x] Design/Implement Teensy/Arduino FSR controller code.
- [x] Document hardware build (frame, panel stack, wiring).

## Milestone 5: Full System Integration [DONE]
- [x] Create standalone kiosk entry point script.
- [x] Implement systemd service for auto-start.
- [x] Final testing and calibration (v1.0.0).

### v2.7.0 Live Testing Milestone
- [x] Full DDC-Deep ML Chart Generation (OnsetNet + SymNet).
- [x] Bobcoin "Fitness Mining" Deep Integration.
- [x] Enhanced FSR Hardware Calibration Utility with History Logging.
- [x] Recursive Submodule Protocol for Total Portability.

### v3.9.0 Industrial Release [DONE]
- [x] Enhanced ML Pipeline with Post-Generation Validator.
- [x] Industrial Diagnostic Suite (Burn-In + Drift Analysis).
- [x] High-Resilience Bobcoin Node Client.
- [x] Unified v3.9.0 Production Documentation.

### v4.0.0 Production Release [DONE]
- [x] Production-Grade ML Vocabulary (Holds, Rolls, Double).
- [x] Robust Multi-Card ALSA Auto-Discovery.
- [x] 60-Minute Production Stress Test Suite.

### v4.1.0 Production Release [DONE]
- [x] Production Heuristic SymNet (Alternating Flow).
- [x] Interactive Hardware Calibration Wizard.
- [x] Unified v4.1.0 Industrial Documentation.
