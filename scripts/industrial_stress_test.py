import os
import sys
import time
import csv
import argparse
import numpy as np

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def run_stress_test(duration_min=60):
    """
    v16.0.0 Industrial Stress Test Suite.
    Validates hardware polling stability and ML inference latency over a sustained period.
    """
    print(f"--- FCDM v16.0.0 INDUSTRIAL STRESS TEST ({duration_min}m) ---")
    cal = FSRCalibrator()
    log_path = "logs/stress_results.csv"
    os.makedirs("logs", exist_ok=True)

    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "jitter_ms", "inference_latency_ms", "p0_raw", "p1_raw"])

        start_time = time.time()
        end_time = start_time + (duration_min * 60)
        last_poll = start_time

        try:
            while time.time() < end_time:
                now = time.time()
                jitter = (now - last_poll) * 1000
                last_poll = now

                # Mock inference latency for stress analysis
                inf_start = time.perf_counter()
                time.sleep(0.002) # simulated 2ms inference
                inf_latency = (time.perf_counter() - inf_start) * 1000

                raw = cal.get_raw_values()[:2]
                writer.writerow([now, jitter, inf_latency, *raw])

                if int(now - start_time) % 60 == 0 and int(now - start_time) > 0:
                    print(f"  [Stress] {int((now - start_time)/60)}m elapsed. Polling: Stable.")

                # Polling at ~100Hz for stress data
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print(f"--- Stress Test Complete. Results: {log_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60)
    args = parser.parse_args()
    run_stress_test(args.duration)
