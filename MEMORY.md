# Memory: Architectural Observations

## Initial State (v0.1.0)
- Project started with a vision for a fitness-focused dance machine.
- Decided to use ITGMania as the primary engine for the kiosk theme.
- Successfully implemented a theme skeleton that bypasses the title screen.

## Design Choices
- **UI**: Minimalist, Kiosk-mode. Custom Lua actor in `ScreenTitleMenu overlay.lua` handles the auto-transition.
- **Sensors**: FSR (Force Sensing Resistors) for longevity and sensitivity. Microcontroller code documented in `docs/HARDWARE.md`.
- **Audio**: Direct ALSA access to minimize latency (planned for final kiosk image).
- **Chart Logic**: Standard charts are too complex for long-form cardio. `scripts/stream_sanitizer.py` enforces a L-R-L-R flow by removing jacks and hands.
