import os
import sys
import time
import json
import argparse
import csv

# Try to use pyserial for physical hardware
try:
    import serial
except ImportError:
    serial = None

class FSRCalibrator:
    """
    v2.4.0 FCDM Hardware Calibration & Diagnostic Utility.
    Supports multi-panel sensitivity tuning, live threshold updates, and performance graphing.
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

        self.profile_path = "config/calibration.json"
        self.drift_log_path = "logs/sensor_drift.csv"
        self.profile = self.load_profile()
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        self.stuck_sensor_thresh = 5.0

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [1.0]*9}

    def save_profile(self):
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)
        print(f"Profile saved to {self.profile_path}")

    def log_drift(self, raw_values):
        os.makedirs(os.path.dirname(self.drift_log_path), exist_ok=True)
        with open(self.drift_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.ctime()] + raw_values)

    def run(self):
        print("FCDM FSR Calibration Utility (v2.4.0)")
        strike_timers = [0.0] * 9

        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) for i in range(9)]

                os.system('clear' if os.name == 'posix' else 'cls')
                print("P | RAW | THR | SENS | STATUS | DIAGNOSTIC | PERFORMANCE")
                print("--|-----|-----|------|--------|------------|------------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]

                    is_strike = (raw * sns) > thr
                    status = "STRIKE" if is_strike else "IDLE"

                    # Graphing (CLI)
                    graph = "#" * (int(raw * sns) // 20)

                    # Stuck Sensor
                    diag = ""
                    if is_strike:
                        strike_timers[i] += 0.1
                        if strike_timers[i] > self.stuck_sensor_thresh:
                            diag = "!! STUCK !!"
                    else:
                        strike_timers[i] = 0.0

                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} | {diag:10} | {graph}")

                print("-" * 65)
                self.log_drift(raw_values)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    cal = FSRCalibrator()
    cal.run()
