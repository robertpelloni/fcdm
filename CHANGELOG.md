# Changelog

## [1.8.0] - 2024-06-08
### Added
- Multi-BPM segment detection in `audio_processor.py`.
- Support for complex tempo shifts in StepMania `#BPMS` tags.

### Changed
- Refined `stream_sanitizer.py` to inject multi-segment BPM strings.
- Incremented version to 1.8.0.

## [1.7.0] - 2024-06-08
### Added
- Remote Serial calibration interface for FSR controller.
- Temperature-based sampling for DDC-Deep step selection.
- Per-panel sensitivity scaling in hardware controller.
- `--difficulty` and `--force` flags for music ingestion.

### Changed
- Improved auto-calibration with signal averaging.
- Optimized `ddc_inference.py` for increased pattern variety.
- Incremented version to 1.7.0.

## [1.6.0] - 2024-06-08
### Added
- Full DDC `SymNet` LSTM port for deep learning step selection.
- Zero-latency tuning: ALSA period/buffer settings and real-time process priority.
- Stress Test suite in `scripts/integration_test.py`.

### Changed
- Refined `ddc_inference.py` for high-volume ingestion stability.
- Incremented version to 1.6.0.

## [1.5.0] - 2024-06-08
### Added
- DDC-Deep signal processing generator (`scripts/ddc_inference.py`) using Mel-spectrogram analysis.
- FSR Calibration Utility (`scripts/calibrate_fsr.py`) for real-time sensor monitoring.

### Changed
- Upgraded music ingestion pipeline to use DDC-Deep as the primary chart generator.
- Updated `docs/HARDWARE.md` with calibration procedures.
- Incremented version to 1.5.0.

## [1.4.0] - 2024-06-08
### Added
- Production-grade ML chart generator (`scripts/dancing2night.py`) using onset detection and circular flow logic.
- Dynamic drift calibration in FSR controller code (`docs/HARDWARE.md`) for stable live testing.

### Changed
- Integrated `Dancing2Night` into the music ingestion pipeline.
- Incremented version to 1.4.0.

## [1.3.0] - 2024-06-07
### Added
- GitHub Actions CI Pipeline (`.github/workflows/ci.yml`).
- Automated end-to-end ingestion tests within CI.
- System dependency documentation for CI runners.
- Structural Submodule Map (`SUBMODULE_MAP.md`).

### Changed
- Promoted project to 1.3.0.
- Verified system stability via comprehensive end-to-end testing.
- Updated documentation with CI details and deployment observations.

## [1.2.0] - 2024-06-07
### Added
- Full Music Ingestion Pipeline (`scripts/ingest_music.py`) to automate song processing.
- UI "Fitness Verified" badges in `FitnessKiosk` theme for sanitized charts.
- Automated skeleton generation for raw audio files.

### Changed
- Integrated ingestion pipeline into `scripts/kiosk-standalone.sh`.
- Updated `StepsDisplayList` to highlight sanitized charts.
- Incremented version to 1.2.0.

## [1.1.0] - 2024-06-07
### Added
- Automated Audio Analysis Pipeline (`scripts/audio_processor.py`) using `librosa`.
- Integration of audio analysis into `scripts/stream_sanitizer.py` for automated BPM and Offset detection.
- Unit tests for the audio processor (`scripts/test_audio_processor.py`).

### Changed
- Updated `VISION.md`, `MEMORY.md`, `DEPLOY.md`, and `IDEAS.md` to reflect the new architecture.
- Incremented version to 1.1.0.

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
