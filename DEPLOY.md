# Deployment & Environment Setup (Staging)

## Software Requirements
- Linux (Ubuntu 22.04+ or Arch recommended)
- ITGMania (included as submodule)
- Python 3.12+
  - `pip install librosa numpy`
- X11/X.org (for Kiosk mode)

## Staging Deployment Steps
1. **Sync Submodules**:
   ```bash
   git submodule update --init --recursive --remote
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt # Or manual install librosa numpy
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
5. **Run Integration Tests**:
   ```bash
   PYTHONPATH=. python3 scripts/integration_test.py
   ```

## Kiosk Manual Launch
```bash
./scripts/kiosk-standalone.sh
```

## Hardware Setup
- Connect Teensy 4.0 (FSR Controller).
- Ensure SoundDrivers=ALSA-sw in `itgmania/Data/Static.ini` or similar.
