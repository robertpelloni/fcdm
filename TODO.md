# TODO: Future Development

## Phase 1: Integration & Polish (v1.3.x) [DONE]
- [x] Connect Stream Sanitizer to a real ML generator output (Dancing2Night).
- [x] Upgrade to DDC-Deep Deep Learning generator (OnsetNet + SymNet).
- [x] Implement temperature-based sampling for ML selection (v1.7.0).
- [ ] Implement multi-BPM support in `audio_processor.py`.
- [ ] Regenerate release zip for v1.3.0.

## Phase 2: Live Testing & Calibration (v1.4.0) [DONE]
- [ ] Conduct Live User Testing (per `docs/LIVE_TESTING.md`).
- [x] Calibrate FSR sensitivity in controller code. (Added dynamic drift calibration)
- [x] Create FSR calibration utility script. (Enhanced with Serial I/O in v1.7.0)
- [x] Finalize Linux/ALSA performance tuning and real-time process priority (v1.6.0).

## Phase 3: Hardware Production (v2.0.0)
- [ ] Finalize industrial frame design.
- [ ] Implement global leaderboards/API integration.
- [ ] Heart rate sync / dynamic difficulty adjustment.

## Completed Tasks
- [x] Add submodules: `bobmania` and `itgmania`.
- [x] Create initial documentation suite.
- [x] Implement "FitnessKiosk" theme skeleton.
- [x] Implement initial "Stream Sanitizer" Python script.
- [x] Document hardware build and controller code.
- [x] Implement full audio analysis pipeline in Python (librosa).
- [x] Integrate Sanitizer and Audio Analysis into a full music ingestion pipeline.
- [x] Establish CI Pipeline for automated testing and validation.
- [x] Refine "FitnessKiosk" theme to show workout-specific stats.
- [x] Override MusicWheelItem to display 1-10 Fitness Levels.
- [x] Implement "Workout Summary" screen.
- [x] Migrate Feedback screen to Pad Panel input.
- [x] Implement systemd service and kiosk entry point.
