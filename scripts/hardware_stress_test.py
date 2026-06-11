import os
import sys
import time
import argparse
import csv
import numpy as np

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def run_hardware_qa(duration_sec=60):
    """
    v9.0.0 1000Hz Hardware Diagnostic.
    Logs FSR jitter and latency spikes to logs/hardware_qa.csv.
    """
    print(f"--- FCDM v9.0.0 HARDWARE STRESS TEST ({duration_sec}s) ---")
    cal = FSRCalibrator()
    log_path = "logs/hardware_qa.csv"
    os.makedirs("logs", exist_ok=True)

    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "jitter_ms", "p0_raw", "p1_raw", "p2_raw", "p3_raw"])

        start_time = time.time()
        last_poll = start_time
        samples = 0

        try:
            while time.time() - start_time < duration_sec:
                now = time.time()
                jitter = (now - last_poll) * 1000
                last_poll = now

                # Poll first 4 pins for stress analysis
                raw = cal.get_raw_values()[:4]
                writer.writerow([now, jitter] + raw)

                samples += 1
                if samples % 1000 == 0:
                    print(f"  [QA] {samples} samples recorded. Jitter: {jitter:.3f}ms")

                # Aim for 1000Hz (1ms sleep)
                time.sleep(0.001)
        except KeyboardInterrupt:
            pass

    print(f"--- QA Complete. Logged to {log_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60)
    args = parser.parse_args()
    run_hardware_qa(args.duration)
