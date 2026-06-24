# Deployment & Environment Setup (v24.1.1 Industrial Onyx Stable)

## Software Requirements
- Linux (Ubuntu LTS or Arch recommended)
- ITGMania (included as submodule)
- Python 3.12+
  - `pip install librosa numpy onnxruntime` (for ML pipeline)
- Teensyduino (for hardware controller)

## Hardware Requirements
- Teensy 4.0
- FSR Sensors (Interlink 402/406)
- Polycarbonate panels (1/2 inch)
- Steel/Aluminum frame (see `docs/HARDWARE.md` for details)

## Running the End-to-End Pipeline
To run the fully integrated generation pipeline (which handles analysis, ML decoding, and stream sanitization):
```bash
./run_pipeline.py
```

## Running the Stress Tests & Latency Profiling
To run a sustained load test verifying system stability and Stream Sanitization latency:
```bash
python3 scripts/industrial_stress_test.py --duration 60 --sim
```

## Running the Sanitizer Manually
```bash
python3 scripts/stream_sanitizer.py input.ssc output.ssc
```
