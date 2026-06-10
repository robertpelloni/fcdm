import os
import sys
import time
import json
import argparse
import csv
import numpy as np

# Try to use pyserial for physical hardware
try:
    import serial
except ImportError:
    serial = None

class FSRCalibrator:
    """
    v3.8.0 FCDM Industrial Hardware Diagnostic Utility.
    Supports Calibration Export for shell integration.
    """
    def __init__(self, port='/dev/ttyACM0', baud=115200):
        self.port = port
        self.baud = baud
        self.ser = None
        if serial:
            try:
                self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
                print(f"Connected to Teensy on {self.port}")
            except Exception as e:
                print(f"Serial error: {e}. Simulation mode enabled.")

        self.profile_dir = "config/profiles"
        self.active_profile = "default"
        self.env_script_path = "scripts/set_fsr_env.sh"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def export_env(self):
        """Generates a shell script to source FSR settings as environment variables."""
        with open(self.env_script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# FCDM Auto-Generated Calibration Environment (v3.8.0)\n\n")

            # Export Thresholds as comma-separated string
            thr_str = ",".join(map(str, self.profile["thresholds"]))
            f.write(f"export FSR_THRESHOLDS=\"{thr_str}\"\n")

            # Export Sensitivities
            sns_str = ",".join(map(str, self.profile["sensitivity"]))
            f.write(f"export FSR_SENSITIVITIES=\"{sns_str}\"\n")

            f.write("\necho \"FCDM: FSR Calibration Environment Loaded.\"\n")

        os.chmod(self.env_script_path, 0o755)
        print(f"Exported environment settings to {self.env_script_path}")

    def run(self):
        print(f"FCDM FSR Utility (v3.8.0) - Mode: CALIB")
        try:
            while True:
                # Simulation
                raw_values = [300 + (i*10) for i in range(9)]
                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM CALIBRATION ---")
                print("P | RAW | THR | STATUS")
                print("--|-----|-----|-------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    status = "STRIKE" if raw > thr else "IDLE"
                    print(f"{p} | {raw:03} | {thr} | {status}")
                if "--sim" in sys.argv: break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--export-env", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    if args.export_env:
        cal.export_env()
    else:
        cal.run()
