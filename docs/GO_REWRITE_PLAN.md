# Milestone 6: Clean-room Go Rewrite Implementation Plan

## Objective
The current Fitness Center Dance Machine (FCDM) orchestrator relies on a series of Python scripts (`run_pipeline.py`, `core_loop.py`, `stream_sanitizer.py`) and bash scripts (`fcdm_launch_production.sh`, `check_system_health.sh`). While functional for v24.1.1 Industrial Onyx Stable, Python introduces latency overhead, and bash scripts are fragile across different Linux distributions.

The goal of Milestone 6 is to rewrite the entire orchestration, hardware management, and ML inference pipeline into a single, compiled, high-performance Go binary.

## Architecture

The Go binary will serve as the master control process, managing the ITGMania subprocess and handling all hardware/software orchestration asynchronously via Go routines.

### Phase 1: Environment & Hardware Subsystems (Migration of Bash)
- **Objective:** Translate `check_system_health.sh` and `fcdm_launch_production.sh` into Go.
- **Tasks:**
  - Implement native Go OS calls to check `/dev/ttyACM0` for the Teensy microcontroller.
  - Implement ALSA card discovery and environment variable injection (`SDL_AUDIODRIVER=alsa`, `ALSA_CARD=0`) directly within the Go process environment before spawning ITGMania.
  - Manage X11 display commands (disabling screen blanking/DPMS) using Go's `os/exec`.

### Phase 2: Pipeline Orchestrator (Migration of Python)
- **Objective:** Replace `run_pipeline.py`.
- **Tasks:**
  - Build a structured Go CLI using a library like `cobra` or `flag` (already stubbed in `src/go-orchestrator/main.go`).
  - Implement the `run_pipeline` logic: initializing the FCDM directories, verifying dependencies, and executing the chart generation loop.
  - Implement the `--sim` flag logic natively to bypass hardware checks during development.

### Phase 3: Remote Web Management (New Feature)
- **Objective:** Enable headless administration of the FCDM kiosk.
- **Tasks:**
  - Embed a lightweight HTTP server (using `net/http` or `gin`) operating on a local port (e.g., `:8080`).
  - Provide REST endpoints to:
    - Reboot the ITGMania process.
    - View current hardware health and sensor telemetry.
    - Upload new audio files to the generation pipeline.
    - Adjust difficulty parameters dynamically.

### Phase 4: High-Performance ML Inference (Deprecating Python ML)
- **Objective:** Remove the Python overhead entirely from chart generation.
- **Tasks:**
  - Translate `stream_sanitizer.py` string-manipulation logic into fast Go byte-slice processing.
  - Utilize CGO bindings (e.g., `github.com/yalue/onnxruntime_go`) to load `lib/models/onset/model.h5` (converted to `.onnx`) directly in Go.
  - Implement the **Coordinate-Aware Kinematic Viterbi Decoder** natively in Go for ultra-fast, zero-latency chart generation.

## Migration Strategy
The rewrite will happen in parallel inside `src/go-orchestrator/`. The existing Python/Bash pipeline will remain the production default until Phase 4 is fully validated by our automated CI/CD (`integration_test.py`, which will be ported to Go test framework `testing` sequentially).
