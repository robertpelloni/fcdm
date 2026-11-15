# Fitness Center Dance Machine (FCDM)

A bespoke software (and hardware) stack for running a dance-game *workout* machine — optimized for sustained, unbroken Zone 2/Zone 3 cardio sessions rather than short rhythm-game bursts. It plays seamless 60+ minute progressive psytrance sets with ML-generated, flow-optimized charts.

This repo is the clean mirror of the project.

## Status

**Personal exergaming project, parked.** Version v24.1.1. Last substantive work: 2026-08-02 (Go ONNX inference merge); last commit: 2026-10-22 (README rewrite). Built for one machine and one purpose; not a general-purpose rhythm game release. (Note: `CHANGELOG.md` dates its releases to June 2024, which does not match the actual 2026 commit history — treat those dates as unreliable.)

## Components

- **Go Orchestrator** (`src/go-orchestrator/`) — a compiled binary that controls the whole machine state: session flow, chart processing, and the stream sanitizer. A prebuilt `fcdm-orchestrator` binary (9.2 MB) sits at the repo root.
- **Kiosk-mode UI** — a stripped-down ITGmania interface for immediate, no-friction use on the machine
- **ML chart generation** — automatic generation of flow-optimized charts using a Kinematic Viterbi Decoder (Go ONNX inference; the older Python `ddc_inference.py` path was deprecated per the July 2026 milestone docs)
- **Stream Sanitizer** — built into the orchestrator (Go-native, no Python interop): post-processes charts to guarantee a safe, strictly alternating cardio flow
- **Hardware Abstraction Layer** (Milestone 8, July 2026) — Go HAL for the machine hardware

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

## Background

Part of Robert Pelloni's long-running dance-game work (StepMania/ITGmania forks, custom dance-machine design), alongside [`bobmania`](https://github.com/robertpelloni/bobmania) and [`itgmania`](https://github.com/robertpelloni/itgmania).

## Docs in this repo

`VISION.md`, `ROADMAP.md`, `TODO.md`, `HANDOFF.md`, `MEMORY.md`, `IDEAS.md`, `DEPLOY.md`, `FOLLOWUP.md`, `CHANGELOG.md`, `docs/`.
