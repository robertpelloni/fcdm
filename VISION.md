# VISION: Fitness Center Dance Machine (v24.1.1)

## The Core Concept
A bespoke software and hardware stack optimized solely for streamlining a workout session. Unlike standard rhythm games designed for short bursts, this machine focuses on sustained, unbroken Zone 2/Zone 3 cardio using seamless 60+ minute progressive psytrance sets.

## Key Features
- **Kiosk-Mode UI**: Stripped-down interface for immediate utility. (Implemented in `itgmania/Themes/FitnessKiosk`)
- **Universal 4/5/SMX Support**: Support for DDR (4-panel), Pump It Up (5-panel), and StepManiaX (5-panel) layouts.
- **1-10 Fitness Scale**: Simplified difficulty mapping. (Normalization logic in `FitnessDifficulties.lua`)
- **ML-Generated Charts**: Automatic generation of flow-optimized charts for long audio sets utilizing a Kinematic Viterbi Decoder.
- **Stream Sanitizer**: Python-based post-processor deeply integrated into `run_pipeline.py` to ensure a safe, strictly alternating cardio flow.
- **Industrial-Grade Hardware**: FSR-based sensors, bulletproof construction, and high-fidelity audio.
- **Zero Latency**: Deeply profiled latency measurements (via `industrial_stress_test.py`) ensure maximum responsiveness under prolonged load.
