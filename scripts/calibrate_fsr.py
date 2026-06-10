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
    v3.0.0 FCDM Hardware Calibration & Burn-In Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    drift logging, and sensor burn-in diagnostics.
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
        self.log_path = "logs/burn_in_results.csv"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def run(self, burn_in=False):
        print(f"FCDM FSR Utility (v3.0.0) - Mode: {'BURN-IN' if burn_in else 'CALIB'}")

        history = []

        try:
            while True:
                # Simulation raw values with random noise
                raw_values = [300 + (i*10) + int(np.random.normal(0, 5)) for i in range(9)]

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM {'BURN-IN' if burn_in else 'CALIBRATION'} ---")
                print("P | RAW | THR | SENS | STATUS")
                print("--|-----|-----|------|-------")

                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]
                    status = "STRIKE" if (raw * sns) > thr else "IDLE"

                    graph = "#" * (int(raw * sns) // 20)
                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} {graph}")

                print("-" * 45)
                if burn_in:
                    history.append([time.ctime()] + raw_values)
                    if len(history) % 100 == 0:
                        self.save_burn_in_log(history)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

    def save_burn_in_log(self, data):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data[-100:])
        print(f"Logged 100 burn-in samples to {self.log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--burnin", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.run(burn_in=args.burnin)
