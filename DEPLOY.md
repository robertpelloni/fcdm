# Deployment & Environment Setup (v24.1.1 Industrial Onyx Stable)

## Software Requirements
- Linux (Ubuntu 22.04+ or Arch recommended)
- ITGMania (included as submodule)
- Python 3.12+
  - `pip install librosa numpy onnxruntime`
- X11/X.org (for Kiosk mode)

## Udev & ALSA Configurations
To run continuously without permission issues on Ubuntu LTS / Arch:

1. **Udev Rules (Teensy & Serial)**:
   Ensure the `itg` or `kiosk` user has access to `/dev/ttyACM0`.
   ```bash
   sudo usermod -aG dialout $USER
   echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="0483", MODE="0666", GROUP="dialout"' | sudo tee /etc/udev/rules.d/99-teensy.rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

2. **ALSA Multi-Card Configuration**:
   Disable PulseAudio/Pipewire for lower latency.
   Force your primary USB DAC to index 0:
   ```bash
   echo 'options snd-usb-audio index=0' | sudo tee -a /etc/modprobe.d/alsa-base.conf
   ```

## Staging Deployment Steps
1. **Sync Submodules**:
   ```bash
   ./fetch-submodules.sh
   ```
2. **Install Dependencies**:
   ```bash
   pip install librosa numpy onnxruntime
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
./scripts/fcdm_launch_production.sh --sim
```
