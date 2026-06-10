# Changelog

## [2.0.0] - 2026-06-09
### Added
- **v2.0.0 Production Milestone**.
- Fully implemented DDC-v2.0.0 (OnsetNet + Ergonomic Selection).
- Deep Bobcoin Node integration for verifiable fitness mining.
- Enhanced FSR calibration tools with industrial drift logging.
- Added production Hardware Calibration Guide.
- Initialized bobcoin submodule in `extern/bobcoin`.

## [2.7.0] - 2026-06-14
### Added
- **v2.7.0 Live Testing Milestone**.
- Fully implemented native SymNet LSTM selection with temperature-based sampling.
- Added "Live Stress Test" mode to `scripts/calibrate_fsr.py` with polling jitter analysis.
- Unified v2.7.0 production stack with automated stress performance logging.

## [2.6.0] - 2026-06-13
### Added
- **v2.6.0 Native ML Milestone**.
- Implemented native ONNX inference loop for SymNet recursive selection.
- Refined OnsetNet feature extraction with high-fidelity windowing.
- Added "Live Test" mode and panel health diagnostics to `scripts/calibrate_fsr.py`.
- Finalized software stack for first live industrial testing.

## [2.5.0] - 2026-06-12
### Added
- **v2.5.0 Performance Diagnostics Milestone**.
- Implemented batch ingestion QA with automated Fitness Level (NPS) calculation.
- Integrated Heart Rate Monitor (HRM) mock into the kiosk UI.
- Added Calibration Profiles and documentation export to `scripts/calibrate_fsr.py`.
- Unified v2.5.0 stack with performance monitoring and HRM visual parity.

## [2.4.0] - 2026-06-11
### Added
- **v2.4.0 High-Fidelity ML Milestone**.
- Finalized recursive LSTM SymNet selection logic in `scripts/ddc_inference.py`.
- Enhanced hardware calibration with real-time performance graphing and high-polling diagnostics.
- Unified v2.4.0 production stack with advanced sensor monitoring.

## [2.3.0] - 2026-06-10
### Added
- **v2.3.0 Production Diagnostics Milestone**.
- Implemented full recursive LSTM selection sequence in `scripts/ddc_inference.py`.
- Added "Stuck Sensor" detection and automated CSV drift logging to `scripts/calibrate_fsr.py`.
- Finalized hardware diagnostic tool suite for physical platform deployment.

## [2.2.0] - 2026-06-09
### Added
- **v2.2.0 Full ML Integration Milestone**.
- Fully implemented SymNet LSTM inference loop in `scripts/ddc_inference.py`.
- Enhanced FSR hardware calibration with sensitivity tuning and live Serial updates.
- Deepened Bobcoin "Fitness Mining" with real CLI hooks and reward caching.
- Updated documentation with v2.2.0 industrial calibration protocols.

## [2.1.0] - 2026-06-09
### Added
- **Production Resilience Update**.
- SymNet LSTM selection architecture support in ONNX.
- Robust error handling and local reward caching for Bobcoin node.
- System-wide v2.1.0 stability improvements.

## [1.0.0] - 2024-05-24
### Added
- Final production release.
- All core features (Fitness 1-10 scale, Kiosk Mode, Stream Sanitizer) verified.

### Changed
- Promoted project to 1.0.0.

## [1.0.0-staging] - 2024-05-24
### Added
- Comprehensive integration test suite (`scripts/integration_test.py`).
- Staging deployment documentation in `DEPLOY.md`.
- Automated dependency installation for staging.

### Changed
- Promoted project to 1.0.0-staging.

## [0.5.0-rc1] - 2024-05-24
### Added
- Linux Kiosk integration: `scripts/kiosk-standalone.sh` and `scripts/dance-machine.service`.
- Live User Testing Protocol (`docs/LIVE_TESTING.md`).

### Changed
- Refined `ScreenFeedback` layout and timing.
- Updated `ROADMAP.md` and `TODO.md` to reflect Release Candidate status.
- Incremented version to 0.5.0-rc1.

## [0.4.0] - 2024-05-24
### Added
- "Workout Summary" screen for `FitnessKiosk` theme, replacing standard evaluation.
- Displays Time, Calories, and Fitness Level in a minimalist layout.
- Integrated Pad Panel input for the Feedback screen (Left/Right/Start).

### Changed
- Updated `metrics.ini` to streamline the post-game flow.
- Incremented version to 0.4.0.

## [0.3.0] - 2024-05-24
### Added
- Custom `MusicWheelItem` for `FitnessKiosk` to display 1-10 fitness levels.
- Custom `StepsDisplayList` for `FitnessKiosk` to display 1-10 fitness levels.
- Synced all submodules to latest tracking commits.
- Added `ScreenFeedback` to collect user workout ratings.

### Changed
- Updated `ROADMAP.md` and `TODO.md` with current progress and future tasks.
- Incremented version to 0.3.0.

## [0.2.0] - 2024-05-24
### Added
- "FitnessKiosk" theme skeleton for ITGMania.
- `itgmania/Themes/FitnessKiosk/metrics.ini` for theme inheritance.
- `itgmania/Themes/FitnessKiosk/Scripts/FitnessDifficulties.lua` for difficulty normalization.
- `itgmania/Themes/FitnessKiosk/BGAnimations/ScreenTitleMenu overlay.lua` for menu bypass.
- `scripts/stream_sanitizer.py` for chart post-processing.
- `scripts/test_stream_sanitizer.py` for automated testing of sanitizer logic.
- `docs/HARDWARE.md` with platform construction and controller code.

### Changed
- Initialized bobmania and itgmania submodules.
- Updated VISION, ROADMAP, TODO, MEMORY, DEPLOY, IDEAS.

## [0.1.0] - 2024-05-24
- Initialized project structure and documentation.
