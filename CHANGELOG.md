# Changelog

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
