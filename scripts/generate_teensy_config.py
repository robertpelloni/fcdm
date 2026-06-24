import os
import sys
import csv
import numpy as np

def generate_config(diag_path="logs/stress_results.csv", output_path="docs/config.h"):
    """
    v23.0.0 Teensy Configuration Generator.
    Analyzes diagnostic data to optimize hardware thresholds and noise filters.
    """
    print(f"--- FCDM v23.0.0 TEENSY CONFIG GENERATOR ---")
    if not os.path.exists(diag_path):
        print(f"Error: {diag_path} not found. Run industrial_stress_test.py first.")
        return

    p0_values = []
    with open(diag_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p0_values.append(float(row['p0_raw']))

    # Calculate optimized threshold (avg baseline + 3*std_dev + margin)
    baseline = np.mean(p0_values)
    noise = np.std(p0_values)
    opt_threshold = int(baseline + (noise * 4) + 100)

    config_content = f"""/*
 * FCDM v23.0.0 Auto-Generated Hardware Configuration
 * Generated from: {diag_path}
 */

#ifndef FCDM_CONFIG_H
#define FCDM_CONFIG_H

const int STRIKE_THRESHOLD = {opt_threshold};
const int DEBOUNCE_MS = 5;
const float SENSITIVITY_DEFAULT = 1.0;

#endif
"""
    with open(output_path, 'w') as f:
        f.write(config_content)

    print(f"[SUCCESS] Optimized config written to {output_path}")
    print(f"  - Baseline Noise: {noise:.2f}")
    print(f"  - Calculated Threshold: {opt_threshold}")

if __name__ == "__main__":
    generate_config()
