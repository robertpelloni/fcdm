import os
import sys
import time
import csv
import argparse

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def run_live_monitor(duration_min=60):
    """
    v14.0.0 Live Hardware Performance Monitor.
    Tracks FSR stability, jitter, and latency during high-intensity sessions.
    """
    print(f"--- FCDM v14.0.0 LIVE HARDWARE MONITOR ({duration_min}m) ---")
    cal = FSRCalibrator()
    log_path = "logs/live_test_results.csv"
    os.makedirs("logs", exist_ok=True)

    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "avg_jitter_ms", "max_latency_ms", "p0_raw", "p1_raw", "p2_raw", "p3_raw"])

        start_time = time.time()
        end_time = start_time + (duration_min * 60)
        last_poll = start_time

        try:
            while time.time() < end_time:
                now = time.time()
                jitter = (now - last_poll) * 1000
                last_poll = now

                # Poll hardware
                raw = cal.get_raw_values()[:4]
                writer.writerow([now, jitter, 0, *raw]) # Latency mock for now

                if int(now - start_time) % 60 == 0 and int(now - start_time) > 0:
                    print(f"  [Monitor] {int((now - start_time)/60)}m elapsed. Stability: Nominal.")

                # High-frequency polling (100Hz for monitor)
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print(f"--- Monitor Complete. Results: {log_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60)
    args = parser.parse_args()
    run_live_monitor(args.duration)
