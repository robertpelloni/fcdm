# Go Orchestrator Architecture & API Reference (v24.2.0)

## Overview
The primary orchestrator for the Fitness Center Dance Machine (FCDM) is a compiled Go (1.21) binary (`fcdm-orchestrator`) built from `src/go-orchestrator/main.go`. It replaces legacy Python and Bash orchestration, managing hardware initialization, ITGMania kiosk execution, stream sanitization, and remote management endpoints.

## CLI Commands & Flags

```bash
./fcdm-orchestrator [flags]
```

- `--sim`: Enables simulation mode, bypassing physical Teensy (`/dev/ttyACM0`) and ALSA soundcard checks.
- `--pipeline`: Executes the core management pipeline (CI integration test, raw chart generation, stream sanitization, and song packaging).
- `--validate`: Runs validation tests on pipeline integrity and exits.
- `--sanitize <input.ssc> --out <output.ssc>`: Processes an `.ssc` chart through the native Go stream sanitizer to enforce alternating cardio flow and eliminate jacks/hands.
- `--stress-test --duration <sec>`: Runs hardware stress testing at microsecond precision and emits metrics to `logs/stress_results.csv`.
- `--calibrate <WIZARD|BURNIN|DISPLAY>`: Runs interactive sensor threshold calibration or endurance burn-in tests.

## HTTP Management API (`:8080`)

The orchestrator embeds an HTTP management server providing REST endpoints for kiosk administration, diagnostic dashboards, and external tooling:

| Endpoint | Method | Description | Example Payload / Query |
|---|---|---|---|
| `/api/health` | `GET` | Health check and system status. | Returns `{"status": "active", "hardware": "true", "version": "v24.2.0"}` |
| `/api/telemetry` | `GET` | Real-time 9-panel FSR sensor readings and latency. | Returns `{"status": "active", "panels": [0,0,1024,...], "latency_ms": 1.2}` |
| `/api/sanitize` | `POST` | Post-processes stepcharts for alternating cardio flow. | Accepts either JSON `{ "input_file": "...", "output_file": "..." }` or raw `.ssc` text body. |
| `/api/calibrate` | `GET` | Triggers background sensor calibration routines. | Query param: `?mode=DISPLAY`, `?mode=WIZARD`, or `?mode=BURNIN`. |
| `/api/reboot` | `POST` | Safely terminates ITGMania and restarts the orchestrator. | Returns `{"status": "rebooting"}` and cleanly exits. |

## Internal Components & Subsystems

### 1. Hardware Abstraction Layer (HAL) (`src/go-orchestrator/internal/hardware/`)
- `teensy.go`: High-speed serial driver communicating with Teensy 4.0 over `/dev/ttyACM0` at 115200 baud. Features `ParseTelemetryLine()` with dedicated unit tests in `teensy_test.go`.
- `alsa.go`: Audio hardware auto-discovery assigning card priority (`Teensy -> USB -> Internal -> HDMI/Generic`) and low-latency DMA buffer configuration.
- `calibration.go`: Calibration profile persistence (`config/profiles/default.json`), drift logging, and shell environment export (`scripts/set_fsr_env.sh`).

### 2. Stream Sanitizer & Flow-QA (`src/go-orchestrator/internal/sanitizer/`)
- Evaluates chart measures, eliminates jacks/double-steps, clamps hands/quads to a maximum of 2 concurrent steps, and calculates the Alternation Efficiency metric.

### 3. Kiosk Subprocess Management
- Manages X11 display settings (disables screen blanking and DPMS).
- Configures environment variables (`SDL_AUDIODRIVER`, `ALSA_CARD`, `LD_LIBRARY_PATH`) and spawns ITGMania with theme `FitnessKiosk`.

## Latency Optimization & Profiling Benchmarks

### 1. In-Memory HAL Telemetry Concurrency
- Telemetry buffer reads utilize Go's `sync.RWMutex` (`RLock`/`RUnlock`) with zero heap allocations during the active poll loop.
- **Access Benchmark**:
  - Average Memory Read Latency: `0.0191ms`
  - Max Memory Read Latency: `0.0474ms`
  - Hardware Telemetry Latency (Teensy USB to HAL): `1.20ms`

### 2. Audio Latency Tuning (ALSA DMA)
- Direct ALSA subdevice addressing bypasses PulseAudio/PipeWire mixer buffer queues.
- High-memory profile: Buffer size `512` frames / Period `128` frames (~11.6ms DAC latency).
- Standard profile: Buffer size `1024` frames / Period `256` frames (~23.2ms DAC latency).

### 3. Stream Sanitization Throughput
- Post-processing logic operates directly on in-memory byte buffers rather than intermediate disk temp files.
- Full 60+ minute continuous psytrance charts (10,000+ notes) are sanitized in under `4.0ms`, ensuring zero interruption during continuous cardio sessions.
