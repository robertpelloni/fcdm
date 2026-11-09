# Changelog

## [24.2.0] - 2026-11-04
### Added
- **v24.2.0 Consolidated Dashboard & System Tray Release**.
- Re-architected `scripts/diagnostic_dashboard.py` into a consolidated single-screen interactive terminal dashboard (curses) featuring:
  - Top system status bar: Go Orchestrator health, ALSA low-latency DMA audio card index, global version.
  - Prominent 3x3 FSR foot pressure matrix with live STRIKE/IDLE status badges, bar graphs, and sensitivity levels.
  - Subsystem telemetry integration: Cardio Continuous Session Timer, HAL latency tracking (< 2ms), Bobcoin flow-bonus node minting, baseline drift monitoring.
  - Interactive hotkey controls: calibration display ('c'), wizard ('w'), burn-in test ('b'), orchestrator reboot ('r'), and toggleable interactive tooltips ('?').
- Implemented **System Tray & Background Daemon Controller** (`scripts/system_tray.py`):
  - Provides system tray graphical icon and interactive CLI daemon fallbacks.
  - Controls lifecycle of Go Orchestrator and background daemons (start, stop, restart, calibration trigger, launch dashboard, clean quit of all servers).
- Harmonized Go Orchestrator native stress testing and stream sanitization:
  - Updated `src/go-orchestrator/main.go` `--stress-test` flag to emit telemetry logs to `logs/stress_results.csv`.
  - Added dual-format support for `/api/sanitize` endpoint (JSON requests and raw SSC text stream).
  - Updated `scripts/test_stream_sanitizer.py` and `scripts/production_stress_runner.sh` to interface directly with the compiled Go orchestrator.

## [24.1.0] - 2024-06-25
### Added
- **v24.1.0 Industrial Onyx Stable Release**.
- Implemented **Coordinate-Aware Kinematic Viterbi Decoder** (8-step lookahead) in `scripts/ddc_inference.py`.
- Enhanced **ALSA Multi-Card management** and prioritization in `scripts/check_system_health.sh`.
- Finalized **Bobcoin Node Client** with robust cross-distro CLI discovery and Flow-Bonus logic.
- Established **Root-Level Production Scripts** (start.sh, build.sh) for industrial orchestration.
- Unified v24.1.0 "Industrial Onyx" release documentation and verified stable production stack.

## [23.0.0] - 2024-06-23
### Added
- **v23.0.0 Industrial Apex Stable Release**.
- Implemented **Windowed Viterbi Kinematic Decoder** in `scripts/ddc_inference.py` for elite sequence ergonomics.
- Integrated **Real ML Load Testing** into `scripts/industrial_stress_test.py`.
- Added **Teensy Config Generator** (`scripts/generate_teensy_config.py`) for automated threshold optimization.
- Unified v23.0.0 "Industrial Apex" release documentation and verified stable production stack.

## [22.0.0] - 2024-06-22
### Added
- **v22.0.0 Industrial Apex Release**.
- Implemented **Multi-Step Lookahead Kinematic Decoder** in `scripts/ddc_inference.py` for elite pattern ergonomics.
- Expanded **Note Vocabulary** for tournament-grade Single and Double charts.
- Enhanced **ALSA Card Prioritization** in `scripts/check_system_health.sh`.
- Finalized **Industrial QA Reporting** for automated hardware certification.
- Unified v22.0.0 "Industrial Apex" stable release documentation.

## [21.0.0] - 2024-06-21
### Added
- **v21.0.0 Industrial Prime Release**.
- Implemented **Global Kinematic Viterbi Decoder** in `scripts/ddc_inference.py` for tournament-grade pattern ergonomics.
- Enhanced **ALSA Multi-Card management** in `scripts/check_system_health.sh` with automated index export.
- Added **Production Stress Runner** orchestrator (`scripts/production_stress_runner.sh`) for stability certification.
- Unified v21.0.0 "Industrial Prime" stable release documentation.

## [20.0.0] - 2024-06-20
### Added
- **v20.0.0 Industrial Diamond Stable Release**.
- Implemented **Viterbi-Inspired Kinematic Decoder** in `scripts/ddc_inference.py` for elite-level ergonomic cost-minimization.
- Added **Industrial QA Report** utility (`scripts/industrial_qa_report.py`) for automated hardware stress test validation.
- Enhanced Bobcoin client with **Flow-Bonus** reward logic for alternation efficiency.
- Unified v20.0.0 industrial release documentation and verified stable production stack.

## [2.0.0] - 2024-06-15
### Added
- **Production ML Release**.
- Implemented **OnsetNet and SymNet Inference** in `scripts/ddc_inference.py` for automated chart generation.
- Integrated **Bobcoin** decentralized currency for verifiable fitness mining rewards.
- Developed comprehensive **Hardware Calibration Suite** (Wizard, Drift, Resonance analysis).
- Optimized kiosk stack for low-latency performance on physical 9-panel platforms.

## [1.0.0] - 2024-05-24
### Added
- Final production release.
- All core features (Fitness 1-10 scale, Kiosk Mode, Stream Sanitizer) verified.
