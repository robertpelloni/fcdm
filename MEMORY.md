# Memory: Architectural Observations (v24.1.0 Industrial Onyx Stable)

## Architecture & Foundational Concepts
The **Fitness Center Dance Machine (FCDM)** is a specialized rhythm game software/hardware stack designed expressly for sustained, unbroken aerobic cardio (Zone 2/3) via 60+ minute progressive psytrance sets, deviating significantly from traditional arcade bursts.

**Engine Layer:**
The application builds upon **ITGMania** (a StepMania 5.1 fork tailored for modern compatibility and network functions) with a custom `FitnessKiosk` minimalist Lua theme to instantly bypass typical selection menus.

**Hardware Stack:**
The machine operates on industrial-grade 9-panel matrix platforms using Force Sensing Resistors (FSRs). The hardware is managed via a Teensy 4.0 microcontroller that communicates physical panel strikes via high-frequency keyboard emulation. The project prioritizes direct ALSA audio pathways over PulseAudio/PipeWire for ultra-low latency response.

**Core Services & Orchestration:**
As of Milestone 6 and 7, the legacy Python and Bash orchestrators (`run_pipeline.py`, `fcdm_launch_production.sh`) have been entirely deprecated and replaced by a high-performance compiled Go binary (`fcdm-orchestrator`). This orchestrator handles ALSA/X11 setup natively, embeds an HTTP management API (port `8080`), and serves as the single point of entry for the system.

## Design Patterns & Decisions
- **Fitness Normalization:** Instead of arbitrary difficulty levels, ITGMania integrates Lua scripts (`FitnessDifficulties.lua`) to convert steps-per-second to a simple 1-10 fitness scale.
- **ML Chart Generation & Kinematics:** Standard rhythmic charts contain dangerous physical patterns for long sessions (e.g. quad hits, jacks). The system previously used Python (`ddc_inference.py`) but has now successfully ported the ONNX inference and Kinematic Viterbi Decoder entirely into the Go Orchestrator (`src/go-orchestrator/internal/inference`). This provides zero-latency chart generation.
- **Stream Sanitization:** Post-processing logic previously handled by `stream_sanitizer.py` has been translated into Go byte-slice processing (`src/go-orchestrator/internal/sanitizer`). This native Go implementation eliminates Python interop overhead and executes significantly faster, keeping processing times well under the 10ms industrial threshold. The pipeline guarantees high Alternation Efficiency and strictly alternating fitness-safe flow patterns.
- **Hardware Simulation Fallbacks:** System bash/python pipelines robustly use `--sim` flags to execute tests cleanly when FSR hardware interfaces (`/dev/ttyACM0`) or advanced ALSA environments are missing.
- **Monetization / Verification:** The project experiments with a built-in decentralized `Bobcoin` (a submodule node client) intended for tracking and rewarding "verifiable fitness mining".

## Ongoing Codebase Trajectory
- **Aggressive Submoduling:** The project relies on deep Git submodules (`bobmania`, `itgmania`, `bobcoin`). To avoid stale proxies or cache locks, a custom `fetch-submodules.sh` exists to selectively fetch dependencies.
- **Production Status:** The main target state is dubbed the "Industrial Onyx Stable" (v24.1.0), aiming for high-availability unattended kiosk deployment.
- **Future Directions:** Extensive `TODO.md` and `IDEAS.md` files suggest future shifts toward a clean-room Go rewrite, VR integration, and real-time heart-rate dynamic adjustments.
