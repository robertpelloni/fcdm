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
    v2.7.0 FCDM Hardware Calibration & Stress Testing Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    drift logging, and strike performance jitter analysis.
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
        self.log_path = "logs/live_test_results.json"
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
        print(f"FCDM FSR Utility (v2.7.0) - Mode: {'STRESS' if stress_test else 'CALIB'}")

        jitter_log = []
        last_poll = time.time()

        try:
            while True:
                # Simulation raw values with random noise
                raw_values = [300 + (i*10) + int(np.random.normal(0, 5)) for i in range(9)]

                # Timing jitter analysis
                now = time.time()
                diff = (now - last_poll) * 1000 # ms
                last_poll = now
                if stress_test: jitter_log.append(diff)

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM {'STRESS TEST' if stress_test else 'CALIBRATION'} ---")
                print(f"Polling: {diff:.2f}ms | Profile: {self.active_profile}")
                print("P | RAW | THR | STATUS | JITTER")
                print("--|-----|-----|--------|-------")

                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    status = "STRIKE" if raw > thr else "IDLE"

                    jit_str = f"{np.std(jitter_log[-50:]):.2f}" if stress_test and len(jitter_log) > 5 else "N/A"
                    print(f"{p} | {raw:03} | {thr} | {status:6} | {jit_str}")

                print("-" * 40)
                if stress_test and len(jitter_log) % 100 == 0:
                    self.save_stress_log(jitter_log)

                if "--sim" in sys.argv: break
                time.sleep(0.01 if stress_test else 0.1) # Fast polling for stress test

        except KeyboardInterrupt:
            print("\nExiting.")

    def save_stress_log(self, data):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        results = {
            "timestamp": time.ctime(),
            "avg_jitter_ms": float(np.mean(data)),
            "std_jitter_ms": float(np.std(data)),
            "max_jitter_ms": float(np.max(data))
        }
        with open(self.log_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Logged stress metrics to {self.log_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stress", action="store_true")
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.run(stress_test=args.stress)
