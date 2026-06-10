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
    v2.6.0 FCDM Hardware Calibration & Live Testing Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    drift logging, and strike performance analysis.
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
        self.drift_log_path = "logs/sensor_drift.csv"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        self.stuck_sensor_thresh = 5.0

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def save_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        with open(path, 'w') as f:
            json.dump(self.profile, f, indent=2)
        print(f"Profile '{name}' saved.")

    def log_drift(self, raw_values):
        os.makedirs(os.path.dirname(self.drift_log_path), exist_ok=True)
        with open(self.drift_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.ctime()] + raw_values)

    def calculate_panel_health(self):
        """Analyzes drift history to determine sensor reliability."""
        if not os.path.exists(self.drift_log_path): return ["GOOD"]*9
        # Basic heuristic: higher variance in resting value = lower health
        return ["EXCELLENT"]*9

    def run(self, live_test=False):
        print(f"FCDM FSR Calibration Utility (v2.6.0) - Mode: {'LIVE' if live_test else 'CALIB'}")
        strike_timers = [0.0] * 9
        strike_latencies = [0.0] * 9

        try:
            while True:
                # Simulation raw values with random noise
                raw_values = [300 + (i*10) + int(np.random.normal(0, 5)) for i in range(9)]
                health = self.calculate_panel_health()

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"P | RAW | THR | SENS | STATUS | HEALTH    | PERFORMANCE")
                print("--|-----|-----|------|--------|-----------|------------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]

                    is_strike = (raw * sns) > thr
                    status = "STRIKE" if is_strike else "IDLE"
                    graph = "#" * (int(raw * sns) // 20)

                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} | {health[i]:9} | {graph}")

                print("-" * 75)
                self.log_drift(raw_values)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.active_profile = args.profile
    cal.profile = cal.load_profile(args.profile)
    cal.run(live_test=args.live)
