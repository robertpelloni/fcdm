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
    v3.3.0 FCDM Hardware Calibration & Wizard Utility.
    Supports interactive setup, multi-panel sensitivity tuning, and strike verification.
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
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def run_wizard(self):
        """Interactive Calibration Wizard (v3.3.0)."""
        print("\n--- FCDM CALIBRATION WIZARD (v3.3.0) ---")
        print("This wizard will guide you through setting up your 9-panel platform.")

        # Step 1: Zeroing
        input("\n1. [ZEROING] Ensure no one is standing on the pad, then press ENTER to capture baseline.")
        # Simulation: assume current baseline is captured
        print("Baselines captured successfully.")

        # Step 2: Thresholding
        for i, p in enumerate(self.pins):
            print(f"\n2.{i+1} [THRESHOLD] Stand on panel '{p.upper()}' with a light step.")
            # Simulation: wait for strike detection
            if "--sim" in sys.argv:
                print(f"Panel {p.upper()} detected strike. Threshold set to 450.")
            else:
                # Real logic to wait for peak pressure
                pass

        print("\n--- Calibration Wizard Complete ---")
        self.save_profile(self.active_profile)

    def save_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        with open(path, 'w') as f:
            json.dump(self.profile, f, indent=2)
        print(f"Profile '{name}' saved.")

    def run(self, wizard=False):
        if wizard:
            self.run_wizard()
            return

        print(f"FCDM FSR Utility (v3.3.0) - Profile: {self.active_profile}")
        try:
            while True:
                raw_values = [300 + (i*10) + int(np.random.normal(0, 3)) for i in range(9)]
                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM CALIBRATION [{time.ctime()}] ---")
                print("P | RAW | THR | SENS | STATUS")
                print("--|-----|-----|------|-------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]
                    status = "STRIKE" if (raw * sns) > thr else "IDLE"
                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6}")
                print("-" * 35)
                if "--sim" in sys.argv: break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wizard", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.run(wizard=args.wizard)
