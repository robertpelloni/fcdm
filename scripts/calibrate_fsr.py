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
            f.write("# FCDM Auto-Generated Calibration Environment (v3.9.0)\n\n")

            # Export Thresholds as comma-separated string
            thr_str = ",".join(map(str, self.profile["thresholds"]))
            f.write(f"export FSR_THRESHOLDS=\"{thr_str}\"\n")

            # Export Sensitivities
            sns_str = ",".join(map(str, self.profile["sensitivity"]))
            f.write(f"export FSR_SENSITIVITIES=\"{sns_str}\"\n")

            f.write("\necho \"FCDM: FSR Calibration Environment Loaded.\"\n")

        os.chmod(self.env_script_path, 0o755)
        print(f"Exported environment settings to {self.env_script_path}")

    def get_raw_values(self):
        """Reads raw values from serial or simulates them."""
        if self.ser:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    return [int(v) for v in line.split(',')]
            except Exception:
                pass
        return [300 + (i*10) + np.random.randint(-5, 5) for i in range(9)]

    def run_burn_in(self, duration_sec=3600):
        """v3.9.0 Industrial Burn-In Test."""
        log_path = "logs/burn_in_diagnostics.csv"
        print(f"Starting {duration_sec}s Burn-In. Logging to {log_path}")

        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            # If file is new or empty, write header
            if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
                writer.writerow(["timestamp", "jitter_ms"] + [f"p{i}_raw" for i in range(9)])

            start_time = time.time()
            last_poll = start_time
            try:
                while time.time() - start_time < duration_sec:
                    now = time.time()
                    jitter = (now - last_poll) * 1000
                    last_poll = now

                    raw_values = self.get_raw_values()
                    writer.writerow([now, jitter] + raw_values)

                    if int(now) % 10 == 0:
                        print(f"  [Burn-In] {int(now - start_time)}s elapsed...")
                    time.sleep(0.01)
            except KeyboardInterrupt:
                print("Burn-In interrupted.")

    def analyze_drift(self):
        """Analyzes sensor fatigue from logs/sensor_drift.csv."""
        log_path = "logs/sensor_drift.csv"
        if not os.path.exists(log_path):
            print("No drift data found.")
            return

        data = np.genfromtxt(log_path, delimiter=',', skip_header=1)
        if data.ndim < 2: return

        print("--- Baseline Drift Analysis ---")
        for i in range(9):
            col = data[:, i+1]
            drift = np.max(col) - np.min(col)
            print(f"Pin {self.pins[i]}: Drift={drift:.2f}, Mean={np.mean(col):.2f}")

    def run_adaptive_mode(self, duration_sec=300):
        """v10.0.0 Industrial Adaptive Calibration and Sensitivity Scaling."""
        print(f"--- FCDM v10.0.0 INDUSTRIAL ADAPTIVE CALIBRATION ({duration_sec}s) ---")
        start_time = time.time()
        hits = [[] for _ in range(9)]

        try:
            while time.time() - start_time < duration_sec:
                raw = self.get_raw_values()
                for i in range(9):
                    if raw[i] > self.profile["thresholds"][i]:
                        hits[i].append(raw[i])

                    # Every 10 hits, adjust threshold
                    if len(hits[i]) >= 10:
                        avg_hit = np.mean(hits[i])
                        # Adjust threshold to 40% of average hit intensity
                        new_thr = int(300 + (avg_hit - 300) * 0.4)
                        print(f"  [Adaptive] Adjusting P{self.pins[i]} Thr: {self.profile['thresholds'][i]} -> {new_thr}")
                        self.profile["thresholds"][i] = new_thr
                        hits[i] = []

                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

        self.save_profile()
        self.export_env()

    def save_profile(self):
        path = os.path.join(self.profile_dir, f"{self.active_profile}.json")
        with open(path, 'w') as f:
            json.dump(self.profile, f, indent=2)

    def run_wizard(self):
        """v4.1.0 Interactive Calibration Wizard."""
        print("--- FCDM v4.1.0 CALIBRATION WIZARD ---")
        print("This wizard will guide you through physical panel strikes.")

        new_thresholds = []
        for i, p in enumerate(self.pins):
            print(f"\n[Step {i+1}/9] Calibrating Panel: {p.upper()}")
            print("Action: STRIKE and HOLD the panel now...")

            samples = []
            for _ in range(20):
                samples.append(self.get_raw_values()[i])
                time.sleep(0.05)

            strike_val = np.max(samples)
            print(f"Detected Strike Value: {strike_val}")

            print("Action: RELEASE the panel...")
            time.sleep(1.0)

            samples = []
            for _ in range(20):
                samples.append(self.get_raw_values()[i])
                time.sleep(0.05)

            idle_val = np.mean(samples)
            print(f"Detected Idle Value: {idle_val:.2f}")

            # Industrial Standard: Threshold = Idle + (Strike - Idle) * 0.4
            thr = int(idle_val + (strike_val - idle_val) * 0.4)
            print(f"Setting {p.upper()} Threshold: {thr}")
            new_thresholds.append(thr)

        self.profile["thresholds"] = new_thresholds
        self.save_profile()
        print("\n[SUCCESS] Calibration Profile Updated.")
        self.export_env()

    def run(self, mode="CALIB"):
        print(f"FCDM FSR Utility (v10.0.0) - Mode: {mode}")
        try:
            while True:
                raw_values = self.get_raw_values()

                if mode == "CALIB":
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
    parser.add_argument("--mode", choices=["CALIB", "BURNIN", "DRIFT", "WIZARD", "ADAPTIVE"], default="CALIB")
    parser.add_argument("--export-env", action="store_true")
    parser.add_argument("--sim", action="store_true")
    parser.add_argument("--duration", type=int, default=60)
    args = parser.parse_args()

    cal = FSRCalibrator()
    if args.export_env:
        cal.export_env()
    elif args.mode == "BURNIN":
        cal.run_burn_in(args.duration)
    elif args.mode == "DRIFT":
        cal.analyze_drift()
    elif args.mode == "WIZARD":
        cal.run_wizard()
    elif args.mode == "ADAPTIVE":
        cal.run_adaptive_mode(args.duration)
    else:
        cal.run(args.mode)
