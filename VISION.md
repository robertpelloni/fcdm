# VISION: Fitness Center Dance Machine

## The Core Concept
A bespoke software and hardware stack optimized solely for streamlining a workout session. Unlike standard rhythm games designed for short bursts, this machine focuses on sustained, unbroken Zone 2/Zone 3 cardio using seamless 60+ minute progressive psytrance sets.

## Key Features
- **Kiosk-Mode UI**: Stripped-down interface for immediate utility. (Implemented skeleton in `itgmania/Themes/FitnessKiosk`)
- **Universal 4/5/SMX Support**: Support for DDR (4-panel), Pump It Up (5-panel), and StepManiaX (5-panel) layouts.
- **1-10 Fitness Scale**: Simplified difficulty mapping. (Normalization logic in `FitnessDifficulties.lua`)
- **ML-Generated Charts**: Automatic generation of flow-optimized charts for long audio sets.
- **Music Ingestion Pipeline**: Fully automated workflow for converting raw audio into fitness-ready charts on startup. (`scripts/ingest_music.py`)
- **Audio Analysis Pipeline**: Automated BPM and downbeat detection for unsynced audio files using `librosa`. (Implemented in `scripts/audio_processor.py`)
- **Automated CI/CD**: Continuous Integration pipeline via GitHub Actions to ensure system stability and chart quality on every commit.
- **Stream Sanitizer**: Python-based post-processor to ensure safe, alternating cardio flow. (Implemented in `scripts/stream_sanitizer.py`)
- **Industrial-Grade Hardware**: FSR-based sensors, bulletproof construction, and high-fidelity audio. (Documented in `docs/HARDWARE.md`)
- **Zero Latency**: Real-time process priority and optimized ALSA buffers for minimal input and audio lag. (Implemented in `scripts/kiosk-standalone.sh`)
