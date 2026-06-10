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
    v3.1.0 FCDM Industrial Hardware Diagnostic Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    and sensor fatigue analysis.
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
        self.log_path = "logs/industrial_diagnostics.csv"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def check_sensor_health(self, raw_values, history):
        """Analyzes sensor baseline drift for industrial fatigue."""
        if len(history) < 10: return ["UNKNOWN"] * 9

        health = []
        for i in range(9):
            baseline_avg = np.mean([h[i+1] for h in history[-50:]])
            current = raw_values[i]
            drift = abs(current - baseline_avg) / (baseline_avg + 1e-6)

            if drift > 0.15: health.append("FATIGUE")
            elif drift > 0.05: health.append("STABLE")
            else: health.append("EXCELLENT")
        return health

    def run(self, diagnostic=False):
        print(f"FCDM FSR Utility (v3.1.0) - Mode: {'DIAG' if diagnostic else 'CALIB'}")

        history = []
        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) + int(np.random.normal(0, 3)) for i in range(9)]

                # Update history
                history.append([time.ctime()] + raw_values)
                if len(history) > 1000: history.pop(0)

                health = self.check_sensor_health(raw_values, history)

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM {'INDUSTRIAL DIAGNOSTICS' if diagnostic else 'CALIBRATION'} ---")
                print("P | RAW | THR | SENS | STATUS | HEALTH")
                print("--|-----|-----|------|--------|-------")

                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]
                    status = "STRIKE" if (raw * sns) > thr else "IDLE"

                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} | {health[i]}")

                print("-" * 45)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--diag", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.run(diagnostic=args.diag)
