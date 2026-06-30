# Fitness Center Dance Machine (FCDM)

A bespoke software and hardware stack optimized solely for streamlining a workout session. Unlike standard rhythm games designed for short bursts, this machine focuses on sustained, unbroken Zone 2/Zone 3 cardio using seamless 60+ minute progressive psytrance sets.

## Features
- **Go Orchestrator**: High-performance, latency-optimized compiled binary controlling the entire machine state.
- **Kiosk-Mode UI**: Stripped-down ITGMania interface for immediate utility.
- **ML-Generated Charts**: Automatic generation of flow-optimized charts utilizing a Kinematic Viterbi Decoder.
- **Stream Sanitizer**: Python-based post-processor to ensure a safe, strictly alternating cardio flow.

## Getting Started
See [DEPLOY.md](DEPLOY.md) for full hardware and software environment setup instructions.

```bash
# Build the Go Orchestrator
cd src/go-orchestrator
go build -o ../../fcdm-orchestrator

# Launch the Machine
cd ../../
./fcdm-orchestrator
```
