import os
import sys
import time
import json
import argparse

# In production, use: import serial
# For verification, we simulate serial.

class MockSerial:
    def __init__(self):
        self.out_buf = []
    def write(self, data):
        print(f"  [SERIAL OUT] {data.decode()}")
        self.out_buf.append(data)
    def in_waiting(self):
        return 0
    def read_line(self):
        return b""

def load_profile(path="config/calibration.json"):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {"thresholds": [450]*9, "sensitivity": [150]*9}

def save_profile(data, path="config/calibration.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Profile saved to {path}")

def run_calibration(sim_mode=True):
    print("FCDM FSR Calibration Utility (v1.7.0)")
    profile = load_profile()

    pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
    ser = MockSerial()

    print("\nControls: [u] Update pin threshold, [s] Save profile, [q] Quit")

    try:
        count = 0
        while count < 5:
            print(f"\n--- Frame {count} ---")
            for i, p in enumerate(pins):
                raw = 300 + (i * 20) + (count * 5)
                status = "STRIKE" if raw > profile["thresholds"][i] else "IDLE"
                print(f"{p} | RAW: {raw:03} | THR: {profile['thresholds'][i]} | {status}")

            # Simulate a user action in frame 2
            if count == 2:
                print("\n> User Action: Update threshold for pin 0 (q) to 320")
                profile["thresholds"][0] = 320
                ser.write(f"t0 320".encode())

            time.sleep(0.5)
            count += 1

        save_profile(profile)
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    run_calibration()
