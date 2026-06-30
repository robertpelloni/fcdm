# Deployment & Environment Setup (v24.1.1 Industrial Onyx Stable)

## Software Requirements
- Linux (Ubuntu LTS or Arch recommended)
- ITGMania (included as submodule)
- Python 3.12+
  - `pip install librosa numpy onnxruntime` (for ML pipeline)
- Go 1.21+ (For Orchestrator)
- Teensyduino (for hardware controller)

## Hardware Requirements
- Teensy 4.0
- FSR Sensors (Interlink 402/406)
- Polycarbonate panels (1/2 inch)
- Steel/Aluminum frame (see `docs/HARDWARE.md` for details)

## Running the End-to-End Pipeline
As of Milestone 6, the Python and Bash orchestration logic has been deprecated. Run the fully compiled Go binary to start the production Kiosk sequence:
```bash
./fcdm-orchestrator
```
To run the automated ML generation and validation pipeline loop:
```bash
./fcdm-orchestrator --pipeline
```

## Running the Stress Tests & Latency Profiling
To run a sustained load test verifying system stability and Stream Sanitization latency:
```bash
python3 scripts/industrial_stress_test.py --duration 60 --sim
```

## Internal HTTP Management
The Go orchestrator exposes an HTTP server on `:8080`.
- Health Check: `curl http://localhost:8080/api/health`
- Reboot ITGMania: `curl http://localhost:8080/api/reboot`
