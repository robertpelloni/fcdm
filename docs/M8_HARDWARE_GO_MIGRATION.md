# Milestone 8: Hardware Integration & Latency Optimization (Go Migration)

## Objective
To entirely eliminate bash and python wrapper scripts used for hardware polling (Teensy/FSRs) and ALSA configuration by migrating their logic into the `fcdm-orchestrator` Go binary. This creates a single point of entry and further reduces systemic polling latency.

## Phases

### Phase 1: ALSA Audio Management
- **Goal:** Manage ALSA environment variables and multi-card prioritization natively.
- **Implementation:** Create `src/go-orchestrator/internal/hardware/alsa.go`. Port the `aplay -l` parsing and card index auto-discovery directly into Go. Export the `SDL_AUDIODRIVER=alsa` and `ALSA_CARD=X` directly into the `exec.Cmd` environment for `itgmania`.

### Phase 2: Teensy FSR Communication
- **Goal:** Read and write directly to `/dev/ttyACM0` via Go.
- **Implementation:** Create `src/go-orchestrator/internal/hardware/teensy.go`. Establish a serial connection to the Teensy 4.0. Handle connection retries, stream parsing (for live hardware dashboard integration), and simulate inputs when run with `--sim`.

### Phase 3: Live Hardware Dashboard Integration
- **Goal:** Serve real-time telemetry from the Teensy via the existing HTTP API.
- **Implementation:** Update the `/api/telemetry` endpoint in `main.go` to stream live parsed data from the new `hardware` package instead of mocked values.

### Phase 4: Validation
- **Goal:** Ensure sub-10ms response times.
- **Implementation:** Run the native Go stress test (`--stress-test`) to validate zero regressions in CPU jitter or system latency.
