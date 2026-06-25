import os
import sys
import time
import argparse
import numpy as np
from scipy.fft import fft

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def analyze_resonance(duration_sec=10):
    """
    v11.0.0 Hardware Resonance Analysis.
    Identifies mechanical vibration frequencies to optimize digital noise filters.
    """
    print(f"--- FCDM v11.0.0 RESONANCE ANALYSIS ({duration_sec}s) ---")
    print("Action: Perform continuous rapid strikes on the panels now...")

    cal = FSRCalibrator()
    fs = 1000 # 1kHz polling
    samples = []

    start_time = time.time()
    while time.time() - start_time < duration_sec:
        # Sample pin 0 (standard reference)
        samples.append(cal.get_raw_values()[0])
        time.sleep(1/fs)

    y = np.array(samples)
    n = len(y)
    yf = fft(y - np.mean(y)) # Remove DC component
    xf = np.linspace(0.0, fs/2, n//2)

    # Identify top 3 resonance peaks
    amps = 2.0/n * np.abs(yf[0:n//2])
    peaks = xf[np.argsort(amps)[-3:][::-1]]

    print("\n--- Resonance Results ---")
    for i, p in enumerate(peaks):
        print(f"  Peak {i+1}: {p:.2f} Hz")

    print("\n[RECOMMENDATION] Configure Low-Pass Filter cutoff below lowest peak.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=10)
    args = parser.parse_args()
    analyze_resonance(args.duration)
