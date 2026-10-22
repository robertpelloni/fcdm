# Fitness Center Dance Machine (FCDM)

A bespoke software (and hardware) stack for running a dance-game *workout* machine — optimized for sustained, unbroken Zone 2/Zone 3 cardio sessions rather than short rhythm-game bursts. It plays seamless 60+ minute progressive psytrance sets with ML-generated, flow-optimized charts.

This repo is the clean mirror of the project.

## Components

- **Go Orchestrator** (`src/go-orchestrator/`) — a compiled binary that controls the whole machine state: session flow, chart processing, and the stream sanitizer
- **Kiosk-mode UI** — a stripped-down ITGmania interface for immediate, no-friction use on the machine
- **ML chart generation** — automatic generation of flow-optimized charts using a Kinematic Viterbi Decoder
- **Stream Sanitizer** — built into the orchestrator (Go-native, no Python interop): post-processes charts to guarantee a safe, strictly alternating cardio flow

Also in the tree: `config/`, `themes/`, `lib/`, `extern/`, `scripts/`, and chart/audio test assets.

## Build & run

See `DEPLOY.md` for the full hardware and software environment setup.

```bash
cd src/go-orchestrator
go build -o ../../fcdm-orchestrator
cd ../../
./fcdm-orchestrator
```

Sanitize an existing chart directly:

```bash
./fcdm-orchestrator --sanitize <input.ssc> --out <output.ssc>
```

## Status

Personal exergaming project by Robert Pelloni — part of his long-running dance-game work (StepMania/ITGmania forks, custom dance-machine design). Built for one machine and one purpose; not a general-purpose rhythm game release.
