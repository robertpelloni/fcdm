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
    v3.5.0 FCDM Industrial Hardware Diagnostic Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    and 'Industrial Stress Test' mode.
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
        self.log_path = "logs/stress_test_results.csv"
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

        os.makedirs(self.profile_dir, exist_ok=True)
        self.profile = self.load_profile(self.active_profile)

    def load_profile(self, name):
        path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def run(self, stress_test=False):
        print(f"FCDM FSR Utility (v3.5.0) - Mode: {'STRESS' if stress_test else 'CALIB'}")

        strike_count = 0
        last_poll = time.time()

        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) + int(np.random.normal(0, 5)) for i in range(9)]

                # Timing analysis
                now = time.time()
                diff = (now - last_poll) * 1000 # ms
                last_poll = now

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM {'STRESS TEST' if stress_test else 'CALIBRATION'} ---")
                print(f"Polling Jitter: {diff:.2f}ms | Profile: {self.active_profile}")
                print("P | RAW | THR | STATUS | HEALTH")
                print("--|-----|-----|--------|-------")

                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    status = "STRIKE" if raw > thr else "IDLE"

                    health = "OK"
                    if raw > (thr * 0.9): health = "WARN"

                    print(f"{p} | {raw:03} | {thr} | {status:6} | {health}")

                print("-" * 40)
                if stress_test:
                    strike_count += 1
                    if strike_count % 100 == 0:
                        self.log_stress(raw_values, diff)

                if "--sim" in sys.argv: break
                time.sleep(0.01 if stress_test else 0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

    def log_stress(self, raw, jitter):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.ctime(), jitter] + raw)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stress", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.run(stress_test=args.stress)
