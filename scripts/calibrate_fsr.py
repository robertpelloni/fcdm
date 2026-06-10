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
    v2.5.0 FCDM Hardware Calibration & Diagnostic Utility.
    Supports multi-panel sensitivity tuning, live threshold updates,
    performance graphing, and Calibration Profiles.
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

    def export_docs(self):
        doc_path = "docs/CALIBRATION_GUIDE.md"
        with open(doc_path, 'a') as f:
            f.write(f"\n\n### Current Thresholds ({time.ctime()})\n")
            f.write("| Panel | Threshold | Sensitivity |\n")
            f.write("|-------|-----------|-------------|\n")
            for i, p in enumerate(self.pins):
                f.write(f"| {p.upper()} | {self.profile['thresholds'][i]} | {self.profile['sensitivity'][i]} |\n")
        print(f"Exported thresholds to {doc_path}")

    def run(self, dry_run=False):
        print(f"FCDM FSR Calibration Utility (v2.5.0) - Profile: {self.active_profile}")
        strike_timers = [0.0] * 9

        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) for i in range(9)]

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"P | RAW | THR | SENS | STATUS | DIAGNOSTIC | PERFORMANCE (Profile: {self.active_profile})")
                print("--|-----|-----|------|--------|------------|------------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]

                    is_strike = (raw * sns) > thr
                    status = "STRIKE" if is_strike else "IDLE"
                    graph = "#" * (int(raw * sns) // 20)

                    diag = ""
                    if is_strike:
                        strike_timers[i] += 0.1
                        if strike_timers[i] > self.stuck_sensor_thresh:
                            diag = "!! STUCK !!"
                    else:
                        strike_timers[i] = 0.0

                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status:6} | {diag:10} | {graph}")

                print("-" * 75)
                self.log_drift(raw_values)

                if dry_run or "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="default", help="Profile name to load")
    parser.add_argument("--export", action="store_true", help="Export current settings to docs")
    parser.add_argument("--sim", action="store_true", help="Simulation mode")
    args = parser.parse_args()

    cal = FSRCalibrator()
    cal.active_profile = args.profile
    cal.profile = cal.load_profile(args.profile)

    if args.export:
        cal.export_docs()
    else:
        cal.run()
