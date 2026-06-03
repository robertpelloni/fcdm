# Roadmap: Fitness Center Dance Machine

## Milestone 1: Foundation & Research [DONE]
- [x] Initialize repository with submodules (BobMania, ITGMania).
- [x] Analyze StepMania/OutFox/ITGMania theme engines.
- [x] Research ML-based stepchart generation (Dance_Diffusion, Omnimix).

## Milestone 2: Minimalist Kiosk Theme [IN PROGRESS]
- [x] Create a stripped-down Lua theme skeleton for ITGMania.
- [x] Implement instant-boot to song selection.
- [x] Implement 1-10 difficulty normalization logic.
- [ ] Wire 1-10 normalization to the Music Wheel UI.
- [ ] Strip evaluation screens to simple workout summaries.

## Milestone 3: ML Pipeline Integration [IN PROGRESS]
- [ ] Develop Python script for audio analysis (BPM, downbeat).
- [ ] Integrate ML chart generator (e.g. Dancing2Night).
- [x] Implement "Stream Sanitizer" to ensure fitness-safe patterns (No hands, no jacks).

## Milestone 4: Hardware Integration [DONE]
- [x] Design/Implement Teensy/Arduino FSR controller code.
- [x] Document hardware build (frame, panel stack, wiring).

## Milestone 5: Full System Integration
- [ ] Create optimized Linux Kiosk image (Openbox, ALSA).
- [ ] Final testing and calibration.
