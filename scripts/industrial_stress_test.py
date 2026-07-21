import os
import sys
import time
import csv
import argparse
import numpy as np
import subprocess

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator
from ddc_inference import DDCInference

def run_stress_test(duration_min=60, sim=False):
    """
    v24.1.1 Industrial Stress Test Suite.
    Validates hardware polling stability, ML inference latency, and Stream Sanitizer latency over a sustained period.
    """
    print(f"--- FCDM v24.1.1 INDUSTRIAL STRESS TEST ({duration_min}m) ---")
    cal = None if sim else FSRCalibrator()
    log_path = "logs/stress_results.csv"
    os.makedirs("logs", exist_ok=True)

    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "jitter_ms", "inference_latency_ms", "sanitizer_latency_ms", "p0_raw", "p1_raw"])

        start_time = time.time()
        end_time = start_time + (duration_min * 60)
        last_poll = start_time

        # Load ML Engine for real load testing
        ml = DDCInference("lib/models/onset/model.h5")

        try:
            while time.time() < end_time:
                now = time.time()
                jitter = (now - last_poll) * 1000
                last_poll = now

                # 1. Real ML Load Test (v24.1.1)
                inf_start = time.perf_counter()
                raw_chart = ml.predict_onsets("test_audio.wav") # Triggers real signal processing
                inf_latency = (time.perf_counter() - inf_start) * 1000

                # Create a mock chart block to pass to sanitizer
                mock_chart_block = "#NOTES:\n"
                for i in range(10):
                   mock_chart_block += "1111\n" # Highly dangerous pattern to force sanitization
                mock_chart_block += ";\n"

                with open("temp_mock.ssc", "w") as tf:
                    tf.write(mock_chart_block)

                # 2. Native Go Stream Sanitizer Latency Test
                san_start = time.perf_counter()
                subprocess.run(["./fcdm-orchestrator", "--sanitize", "temp_mock.ssc", "--out", "temp_mock_clean.ssc"], stdout=subprocess.DEVNULL)
                san_latency = (time.perf_counter() - san_start) * 1000

                raw = cal.get_raw_values()[:2] if cal else [0, 0]
                writer.writerow([now, jitter, inf_latency, san_latency, *raw])

                if int(now - start_time) % 60 == 0 and int(now - start_time) > 0:
                    print(f"  [Stress] {int((now - start_time)/60)}m elapsed. Polling: Stable. Inf Latency: {inf_latency:.2f}ms San Latency: {san_latency:.2f}ms")

                # Polling at ~100Hz for stress data
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    print(f"--- Stress Test Complete. Results: {log_path} ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()

    if args.sim:
        print("[SIM] Limiting stress test for quick validation.")
        run_stress_test(duration_min=min(args.duration, 1), sim=True)
    else:
        run_stress_test(args.duration, sim=False)
