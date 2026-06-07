# Memory: Architectural Observations

## Initial State (v0.1.0)
- Project started with a vision for a fitness-focused dance machine.
- Decided to use ITGMania as the primary engine for the kiosk theme.
- Successfully implemented a theme skeleton that bypasses the title screen.

## Fitness Level Normalization (v0.3.0)
- Implemented a 1-10 fitness scale based on Notes Per Second (NPS).
- Logic is encapsulated in `Scripts/FitnessDifficulties.lua`.
- Wired this scale into the `MusicWheelItem` and `StepsDisplayList` to replace standard difficulty meters.
- This ensures the user sees a consistent fitness-oriented metric regardless of the underlying chart's original difficulty rating.

## CI/CD Integration (v1.3.0)
- Established GitHub Actions workflow in `.github/workflows/ci.yml`.
- Automates dependency installation, submodule fetching, and full test suite execution.
- Includes end-to-end verification of the music ingestion pipeline.

## Full Ingestion Pipeline (v1.2.0)
- Automated the entire music ingestion process with `scripts/ingest_music.py`.
- Connected the audio processor and sanitizer into a single-command workflow triggered at boot.
- Added UI badges in the `FitnessKiosk` theme to identify "Fitness Verified" charts.

## Audio Analysis & Sanitization (v1.1.0)
- Integrated `librosa` for automated audio analysis.
- `scripts/audio_processor.py` provides BPM and downbeat detection.
- `scripts/stream_sanitizer.py` now leverages this data to automatically sync charts if timing data is missing.

## Design Choices
- **UI**: Minimalist, Kiosk-mode. Custom Lua actor in `ScreenTitleMenu overlay.lua` handles the auto-transition.
- **Sensors**: FSR (Force Sensing Resistors) for longevity and sensitivity. Microcontroller code documented in `docs/HARDWARE.md`.
- **Audio**: Direct ALSA access to minimize latency (planned for final kiosk image).
- **Chart Logic**: Standard charts are too complex for long-form cardio. `scripts/stream_sanitizer.py` enforces a L-R-L-R flow by removing jacks and hands.
- **Theme Inheritance**: `FitnessKiosk` falls back to `_fallback` but is intended to work alongside `Simply Love` if needed (though current implementation overrides core parts).
