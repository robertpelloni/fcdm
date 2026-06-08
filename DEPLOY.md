# Deployment & Environment Setup (Staging)

## Software Requirements
- Linux (Ubuntu 22.04+ or Arch recommended)
- ITGMania (fetched via `fetch-submodules.sh`)
- Python 3.12+
  - `pip install librosa numpy tensorflow onnxruntime pyserial`
- X11/X.org (for Kiosk mode)

## Staging Deployment Steps
1. **Sync Submodules**:
   ```bash
   bash fetch-submodules.sh --shallow
   ```
2. **Install Dependencies**:
   ```bash
   pip install librosa numpy tensorflow onnxruntime pyserial
   ```
3. **Setup Theme Symlink**:
   ```bash
   ln -s ../../themes/FitnessKiosk itgmania/Themes/FitnessKiosk
   ```
4. **Configure Systemd Service**:
   ```bash
   sudo cp scripts/dance-machine.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable dance-machine
   ```
5. **Prepare ML Models**:
   The DDC models are in a legacy format. Convert them for the modern environment:
   ```bash
   python3 scripts/convert_models.py
   ```

6. **Run Integration Tests**:
   ```bash
   PYTHONPATH=. python3 scripts/integration_test.py
   ```

## Kiosk Manual Launch
```bash
./scripts/kiosk-standalone.sh
```

## Hardware Setup
- Connect Teensy 4.0 (FSR Controller).
- Run calibration utility: `PYTHONPATH=. python3 scripts/calibrate_fsr.py`
- Ensure SoundDrivers=ALSA-sw in `itgmania/Data/Static.ini` or similar.
