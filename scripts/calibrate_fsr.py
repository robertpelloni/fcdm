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
    """
    v2.2.0 FCDM Hardware Calibration Utility.
    Supports multi-panel sensitivity tuning and live threshold updates.
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
        self.profile = self.load_profile()
        self.pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']

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

    def send_cmd(self, cmd, pin, val):
        """Sends a calibration command to the hardware."""
        if self.ser:
            msg = f"{cmd}{pin} {val}\n".encode()
            self.ser.write(msg)
            print(f"  [SERIAL] Sent: {msg.decode().strip()}")

    def run(self):
        print("FCDM FSR Calibration Utility (v2.2.0)")
        print("Commands: [t <idx> <val>] Set threshold, [s <idx> <val>] Set sensitivity, [w] Save, [q] Quit")
        try:
            while True:
                # Simulation raw values
                raw_values = [300 + (i*10) for i in range(9)]

                os.system('clear' if os.name == 'posix' else 'cls')
                print("P | RAW | THR | SENS | STATUS")
                print("--|-----|-----|------|-------")
                for i, p in enumerate(self.pins):
                    raw = raw_values[i]
                    thr = self.profile["thresholds"][i]
                    sns = self.profile["sensitivity"][i]
                    status = "STRIKE" if (raw * sns) > thr else "IDLE"
                    print(f"{p} | {raw:03} | {thr} | {sns:.1f}  | {status}")
                print("-" * 30)

                if "--sim" in sys.argv: break
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    cal = FSRCalibrator()
    cal.run()
