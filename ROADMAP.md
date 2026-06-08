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
- [x] Develop Python script for audio analysis (BPM, downbeat) using librosa. (Enhanced in v1.1.0)
- [x] Integrate ML chart generator (e.g. Dancing2Night).
- [x] Implement "Stream Sanitizer" to ensure fitness-safe patterns (No hands, no jacks).
- [x] Integrate Sanitizer and Audio Analysis into a full music ingestion pipeline (v1.2.0).
- [x] Establish CI Pipeline for automated testing and validation (v1.3.0).
- [x] Implement Dancing2Night production-grade ML generator (v1.4.0).

## Milestone 4: Hardware Integration [DONE]
- [x] Design/Implement Teensy/Arduino FSR controller code. (Enhanced with drift calibration in v1.4.0)
- [x] Document hardware build (frame, panel stack, wiring).

## Milestone 5: Full System Integration [DONE]
- [x] Create standalone kiosk entry point script.
- [x] Implement systemd service for auto-start.
- [x] Final testing and calibration (v1.0.0).
