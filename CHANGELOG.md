# Changelog

## [2.0.0] - 2024-05-25
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

## [2.6.0] - 2024-05-25
### Added
- **v2.6.0 Native ML Milestone**.
- Implemented native ONNX inference loop for SymNet recursive selection.
- Refined OnsetNet feature extraction with high-fidelity windowing.
- Added "Live Test" mode and panel health diagnostics to `scripts/calibrate_fsr.py`.
- Finalized software stack for first live industrial testing.

## [2.9.0] - 2026-06-14
### Added
- **v2.9.0 Resilient Production Milestone**.
- Fully implemented recursive LSTM hidden-state tracking in SymNet.
- Refined OnsetNet feature windowing architecture for production weights.
- Added reward caching and automated cache flushing to Bobcoin client.
- Enhanced hardware stress testing with polling jitter analysis.

## [3.5.0] - 2024-05-28
### Added
- **v3.5.0 ONNX Parity Milestone**.
- Fully transitioned to native recursive LSTM SymNet selection with high-fidelity sampling.
- Refined OnsetNet windowing and hidden-state management for production weights.
- Added 'Industrial Stress Test' mode to `scripts/calibrate_fsr.py` with polling jitter analysis.
- Unified v3.5.0 production stack with automated health warnings.

## [3.4.0] - 2024-05-27
### Added
- **v3.4.0 Production Parity Milestone**.
- Fully implemented native SymNet recursive LSTM selection with hidden-state tracking.
- Refined OnsetNet windowing and temperature-based pattern sampling (T=0.8).
- Added 'Industrial Burn-In' diagnostic mode for automated hardware stress testing.
- Enhanced Fitness Flow QA with alternation efficiency analysis.

## [3.3.0] - 2024-05-26
### Added
- **v3.3.0 Resilience Milestone Release**.
- Disk-backed JSON transaction queue for Bobcoin rewards (node resilience).
- Interactive 'Calibration Wizard' with physical strike verification.
- Flow-aware ML chart generation with 'Fitness Flow Score' QA.
- Automated ALSA hardware buffer analysis.

## [3.1.0] - 2024-05-26
### Added
- **v3.1.0 Industrial Release**.
- Implemented multiprocessing bulk ingestion in `scripts/ingest_music.py`.
- Optimized kiosk launch with ALSA buffer tuning and real-time scheduling.
- Added 'Industrial Diagnostics' for sensor fatigue analysis.
- Finalized production stability for high-volume physical deployments.

## [3.0.0] - 2024-05-25
### Added
- **v3.0.0 Physical Milestone Release**.
- Fully native recursive LSTM SymNet selection with high-fidelity weights.
- Advanced Teensy controller code with dynamic noise filtering.
- 'Burn-In' diagnostic mode for new physical platform assembly.
- Finalized software stack for industrial deployment.

## [2.8.0] - 2024-05-25
### Added
- **v2.8.0 Production ML Milestone**.
- Full support for production weights (.h5 and .onnx) in `scripts/ddc_inference.py`.
- Automated "Flow Analysis" QA for generated charts.
- System health check script for pre-testing verification.
- Finalized live testing benchmarks in documentation.

## [2.5.0] - 2024-05-25
### Added
- **v2.5.0 Performance Diagnostics Milestone**.
- Implemented batch ingestion QA with automated Fitness Level (NPS) calculation.
- Integrated Heart Rate Monitor (HRM) mock into the kiosk UI.
- Added Calibration Profiles and documentation export to `scripts/calibrate_fsr.py`.
- Unified v2.5.0 stack with performance monitoring and HRM visual parity.

## [2.4.0] - 2024-05-25
### Added
- **v2.4.0 High-Fidelity ML Milestone**.
- Finalized recursive LSTM SymNet selection logic in `scripts/ddc_inference.py`.
- Enhanced hardware calibration with real-time performance graphing and high-polling diagnostics.
- Unified v2.4.0 production stack with advanced sensor monitoring.

## [2.3.0] - 2024-05-25
### Added
- **v2.3.0 Production Diagnostics Milestone**.
- Implemented full recursive LSTM selection sequence in `scripts/ddc_inference.py`.
- Added "Stuck Sensor" detection and automated CSV drift logging to `scripts/calibrate_fsr.py`.
- Finalized hardware diagnostic tool suite for physical platform deployment.

## [2.2.0] - 2024-05-25
### Added
- **v2.2.0 Full ML Integration Milestone**.
- Fully implemented SymNet LSTM inference loop in `scripts/ddc_inference.py`.
- Enhanced FSR hardware calibration with sensitivity tuning and live Serial updates.
- Deepened Bobcoin "Fitness Mining" with real CLI hooks and reward caching.
- Updated documentation with v2.2.0 industrial calibration protocols.

## [2.1.0] - 2024-05-25
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
