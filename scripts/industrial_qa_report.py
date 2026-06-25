import os
import sys
import csv
import numpy as np

def generate_report(log_path="logs/stress_results.csv"):
    """
    v22.0.0 Industrial QA Report Generator.
    Parses stress test logs and generates a pass/fail certificate.
    """
    print(f"--- FCDM v20.0.0 INDUSTRIAL QA REPORT ---")
    if not os.path.exists(log_path):
        print(f"Error: Log file {log_path} not found.")
        return

    jitters = []
    latencies = []

    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jitters.append(float(row['jitter_ms']))
            latencies.append(float(row['inference_latency_ms']))

    # 1. Jitter Analysis
    avg_jitter = np.mean(jitters)
    max_jitter = np.max(jitters)
    jitter_pass = max_jitter < 10.0

    # 2. Inference Latency
    avg_inf = np.mean(latencies)
    inf_pass = avg_inf < 20.0

    print(f"Log Duration: {len(jitters) / 100:.1f} minutes (est)")
    print(f"Average Jitter: {avg_jitter:.2f} ms")
    print(f"Peak Jitter: {max_jitter:.2f} ms")
    print(f"Average Inference: {avg_inf:.2f} ms")

    status = "PASS" if (jitter_pass and inf_pass) else "FAIL"
    print(f"\nFINAL STATUS: [{status}]")

    if status == "FAIL":
        if not jitter_pass: print("  - REASON: Peak jitter exceeded 10ms threshold.")
        if not inf_pass: print("  - REASON: Average inference exceeded 20ms threshold.")

if __name__ == "__main__":
    generate_report(sys.argv[1] if len(sys.argv) > 1 else "logs/stress_results.csv")
