import os
import sys
import time
import argparse
import subprocess
import numpy as np

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ddc_inference import DDCInference
from calibrate_fsr import FSRCalibrator

def run_stress_test(duration_min=60, sim=False):
    """
    v4.0.0 Production Stress Test.
    Simultaneously runs ML inference loops and hardware diagnostic polling.
    """
    print(f"--- FCDM v4.0.0 STRESS TEST ({duration_min} min) ---")
    start_time = time.time()
    end_time = start_time + (duration_min * 60)

    # Initialize components
    cal = FSRCalibrator()
    # Mock models for stability test if weights missing
    ONSET_WEIGHTS = "lib/models/onset/model.h5"
    SYM_WEIGHTS = "lib/models/dance-single_Expert/model.h5"
    ml = DDCInference(ONSET_WEIGHTS, SYM_WEIGHTS)

    # Use a dummy audio file for ML stress
    dummy_audio = "test_audio.wav"
    if not os.path.exists(dummy_audio):
        # Create a tiny silent wav for testing if needed
        import wave
        with wave.open(dummy_audio, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(44100)
            f.writeframes(b'\x00' * 88200) # 1 second of silence

    iterations = 0
    try:
        while time.time() < end_time:
            # 1. ML Stress: Run Onset Detection
            onsets = ml.predict_onsets(dummy_audio)

            # 2. Hardware Stress: Poll FSR values
            raw = cal.get_raw_values()

            iterations += 1
            elapsed = time.time() - start_time
            if iterations % 10 == 0:
                print(f"  [Stress] Elapsed: {elapsed/60:.1f}m | Iterations: {iterations} | Last FSR: {raw[0]}")

            if sim and iterations > 5: break
            time.sleep(0.1)

        print(f"--- Stress Test Complete (Success) ---")
    except Exception as e:
        print(f"--- Stress Test FAILED: {e} ---")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()
    run_stress_test(args.duration, args.sim)
