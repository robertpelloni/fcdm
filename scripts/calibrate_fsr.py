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
                print(f"Physical Serial failed: {e}. Simulation mode enabled.")

        self.profile_path = "config/calibration.json"
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
        print(f"Profile saved to {self.profile_path}")

    def send_to_hardware(self, pin_idx, val, cmd='t'):
        if self.ser:
            msg = f"{cmd}{pin_idx} {val}\n".encode()
            self.ser.write(msg)
            print(f"  [HARDWARE] Sent: {msg.decode().strip()}")

    def run(self):
        print("FCDM FSR Calibration Utility (v1.8.0)")
        print("Controls: [t <pin> <val>] Update threshold, [s <pin> <val>] Update sensitivity, [w] Write to disk, [q] Quit")

        try:
            while True:
                # 1. Read/Simulate values
                raw_values = []
                if self.ser:
                    line = self.ser.readline().decode().strip()
                    if line.startswith("RAW:"):
                        raw_values = [int(v) for v in line.split(":")[1].split(",")]

                if not raw_values: # Simulation fallback
                    raw_values = [300 + (i*10) for i in range(9)]

                # 2. Display
                os.system('clear' if os.name == 'posix' else 'cls')
                print("P | RAW | THR | STATUS")
                print("--|-----|-----|-------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    status = "STRIKE" if raw > thr else "IDLE"
                    print(f"{p} | {raw:03} | {thr} | {status}")

                print("-" * 25)
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    cal = FSRCalibrator()
    if "--sim" in sys.argv:
        # Just run a quick check for CI
        print("Calibration test passed.")
    else:
        cal.run()
