import os
import sys
import time
import json
import argparse

# Try to use pyserial for physical hardware
try:
    import serial
except ImportError:
    serial = None

class FSRCalibrator:
    def __init__(self, port='/dev/ttyACM0', baud=115200):
        self.port = port
        self.baud = baud
        self.ser = None
        if serial:
            try:
                self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
                print(f"Connected to Teensy on {self.port}")
            except Exception as e:
                print(f"Serial failed: {e}. Simulation mode.")

        self.profile_path = "config/calibration.json"
        self.history_path = "logs/calibration_history.log"
        self.profile = self.load_profile()
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        return {"thresholds": [450]*9, "sensitivity": [150]*9}

    def save_profile(self):
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile, f, indent=2)

        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
        with open(self.history_path, 'a') as f:
            f.write(f"{time.ctime()}: Updated {json.dumps(self.profile)}\n")
        print(f"Profile saved and logged.")

    def run(self):
        print("FCDM FSR Calibration Utility (v1.9.0)")
        print("Multi-Panel Visualization Mode")
        try:
            while True:
                # Simulation values (raw sensor data)
                raw_values = [300 + (i*10) + int(np.random.normal(0,5)) if 'np' in globals() else 300+(i*10) for i in range(9)]

                os.system('clear' if os.name == 'posix' else 'cls')
                print(f"--- FCDM CALIBRATION [{time.ctime()}] ---")
                print("PANEL | RAW | THR | STATUS")
                print("--------------------------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    status = "STRIKE" if raw > thr else "IDLE"
                    bar = "#" * (raw // 20)
                    print(f"{p.upper()}     | {raw:03} | {thr} | {status} {bar}")
                print("--------------------------")
                print("[W] Write  [Q] Quit")

                if "--sim" in sys.argv: break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    import numpy as np # For noise simulation
    cal = FSRCalibrator()
    cal.run()
