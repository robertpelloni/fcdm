# VISION: Fitness Center Dance Machine (v24.2.0)

## The Core Concept
A bespoke software and hardware stack optimized solely for streamlining a workout session. Unlike standard rhythm games designed for short bursts, this machine focuses on sustained, unbroken Zone 2/Zone 3 cardio using seamless 60+ minute progressive psytrance sets.

## Key Features
- **Kiosk-Mode UI**: Stripped-down interface for immediate utility. (Implemented in `itgmania/Themes/FitnessKiosk`)
- **Consolidated Dashboard & System Tray**: Consolidated single-page interactive monitoring console and system tray manager for real-time telemetry, calibration, and server process control.
- **Universal 4/5/SMX Support**: Support for DDR (4-panel), Pump It Up (5-panel), and StepManiaX (5-panel) layouts.
- **1-10 Fitness Scale**: Simplified difficulty mapping. (Normalization logic in `FitnessDifficulties.lua`)
- **ML-Generated Charts**: Automatic generation of flow-optimized charts for long audio sets utilizing a Kinematic Viterbi Decoder natively in the Go Orchestrator.
- **Stream Sanitizer**: Go-native post-processor deeply integrated into the Orchestrator HTTP API (`/api/sanitize`) to ensure a safe, strictly alternating cardio flow.
- **Industrial-Grade Hardware**: FSR-based sensors, bulletproof construction, and high-fidelity audio.
- **Zero Latency**: Deeply profiled latency measurements (via `fcdm-orchestrator --stress-test`) ensure maximum responsiveness under prolonged load.
