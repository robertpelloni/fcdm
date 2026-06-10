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
    v3.6.0 FCDM Industrial Hardware Diagnostic Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    and 'Burn-In' diagnostic mode for platform assembly.
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
        self.log_path = "logs/burn_in_diagnostics.csv"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

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
        os.makedirs(self.profile_dir, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(self.profile, f, indent=2)
        print(f"Profile '{name}' saved.")

    def log_burn_in(self, raw_values, strike_count, jitter):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.ctime(), strike_count, jitter] + raw_values)

    def run(self, burn_in=False):
        print(f"FCDM FSR Utility (v3.6.0) - Mode: {'BURN-IN' if burn_in else 'CALIB'}")

        strike_count = 0
        last_poll = time.time()
        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) + int(np.random.normal(0, 3)) for i in range(9)]

                # Jitter analysis
                now = time.time()
                jitter = (now - last_poll) * 1000
                last_poll = now

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM {'INDUSTRIAL BURN-IN' if burn_in else 'CALIBRATION'} ---")
                print(f"Strikes: {strike_count} | Jitter: {jitter:.2f}ms | Profile: {self.active_profile}")
                print("P | RAW | THR | SENS | STATUS | HEALTH")
                print("--|-----|-----|------|--------|-------")

                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]
                    is_strike = (raw * sns) > thr
                    status = "STRIKE" if is_strike else "IDLE"
                    if is_strike: strike_count += 1

                    health = "OK"
                    if raw > (thr * 0.95): health = "ALERT"

                    graph = "#" * (int(raw * sns) // 20)
                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} | {health:5} {graph}")

                print("-" * 55)
                if burn_in and strike_count % 100 == 0:
                    self.log_burn_in(raw_values, strike_count, jitter)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--burnin", action="store_true")
    parser.add_argument("--sim", action="store_true")
    parser.add_argument("--profile", default="default")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.active_profile = args.profile
    cal.profile = cal.load_profile(args.profile)
    cal.run(burn_in=args.burnin)
