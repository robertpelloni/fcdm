# Deployment & Environment Setup

## Software Requirements
- Linux (Ubuntu LTS or Arch recommended)
- ITGMania (included as submodule)
- Python 3.x
  - `pip install librosa numpy` (for future pipeline)
- Teensyduino (for hardware controller)

## Hardware Requirements
- Teensy 4.0
- FSR Sensors (Interlink 402/406)
- Polycarbonate panels (1/2 inch)
- Steel/Aluminum frame (see `docs/HARDWARE.md` for details)

## Running the Sanitizer
```bash
python3 scripts/stream_sanitizer.py input.ssc output.ssc
```
