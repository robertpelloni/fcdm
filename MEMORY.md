[PROJECT_MEMORY]

## Architecture & Foundational Concepts
The **Fitness Center Dance Machine (FCDM)** is a specialized rhythm game software/hardware stack designed expressly for sustained, unbroken aerobic cardio (Zone 2/3) via 60+ minute progressive psytrance sets, deviating significantly from traditional arcade bursts.

**Engine Layer:**
The application builds upon **ITGMania** (a StepMania 5.1 fork tailored for modern compatibility and network functions) with a custom `FitnessKiosk` minimalist Lua theme to instantly bypass typical selection menus.

**Hardware Stack:**
The machine operates on industrial-grade 9-panel matrix platforms using Force Sensing Resistors (FSRs). The hardware is managed via a Teensy 4.0 microcontroller that communicates physical panel strikes via high-frequency keyboard emulation. The project prioritizes direct ALSA audio pathways over PulseAudio/PipeWire for ultra-low latency response.

**Core Services & Orchestration:**
A central python orchestrator (`run_pipeline.py`) manages the end-to-end operation, encapsulating processes through a series of shell and python scripts. Essential runtime orchestration is handled via `fcdm_launch_production.sh`, spanning the ITGMania process, Bobcoin Node Watcher, and Live Hardware monitors. As of v24.1.1, a clean-room Go rewrite skeleton has been initialized to transition toward higher performance orchestration.

## Design Patterns & Decisions
- **Fitness Normalization:** Instead of arbitrary difficulty levels, ITGMania integrates Lua scripts (`FitnessDifficulties.lua`) to convert steps-per-second to a simple 1-10 fitness scale.
- **ML Chart Generation & Kinematics:** Standard rhythmic charts contain dangerous physical patterns for long sessions (e.g. quad hits, jacks). The system uses machine learning inference (OnsetNet, SymNet via `ddc_inference.py`) equipped with a **Coordinate-Aware Kinematic Viterbi Decoder** (introduced in v24.1.0/v24.1.1). This decoder performs an 8-step lookahead to optimize physical pathing, avoiding erratic crossovers and ensuring elite tournament-grade pattern vocabulary that is safe for prolonged exertion.
- **Stream Sanitization:** Post-processing python utilities (`stream_sanitizer.py`) ensure that the resulting charts have high Alternation Efficiency (strict Left-Right-Left-Right flow), removing physical anomalies that might disrupt pacing.
- **Hardware Simulation Fallbacks:** System bash/python pipelines robustly use `--sim` flags to execute tests cleanly when FSR hardware interfaces (`/dev/ttyACM0`) or advanced ALSA environments are missing.
- **Monetization / Verification:** The project experiments with a built-in decentralized `Bobcoin` (a submodule node client) intended for tracking and rewarding "verifiable fitness mining".

## Ongoing Codebase Trajectory
- **Aggressive Submoduling:** The project relies on deep Git submodules (`bobmania`, `itgmania`, `bobcoin`). To avoid stale proxies or cache locks, a custom `fetch-submodules.sh` exists to selectively fetch dependencies.
- **Production Status:** The main target state is dubbed the "Industrial Onyx Stable" (v24.1.1), aiming for high-availability unattended kiosk deployment.
- **Future Directions:** Extensive `ROADMAP.md` and `TODO.md` files suggest future shifts toward a full Go rewrite, VR integration, and real-time heart-rate dynamic adjustments.
