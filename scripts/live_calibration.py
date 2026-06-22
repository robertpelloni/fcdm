import os
import sys
import subprocess
import time
import argparse

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def run_live_setup(sim=False):
    """
    v15.0.0 Live Hardware Calibration and Setup Tool.
    Automates the sequence: ALSA Discovery -> FSR Wizard -> Drift Analysis.
    """
    print("--- FCDM v15.0.0 LIVE HARDWARE SETUP ---")

    # 1. System Health & ALSA Card Selection
    print("\n[1/3] Running System Health & Audio Auto-Discovery...")
    health_cmd = ["bash", "scripts/check_system_health.sh"]
    if sim: health_cmd.append("--sim")
    subprocess.run(health_cmd)

    # 2. Interactive Calibration Wizard
    print("\n[2/3] Launching FSR Calibration Wizard...")
    cal = FSRCalibrator()
    if sim:
        print("  [SIM] Skipping interactive wizard in simulation mode.")
    else:
        cal.run_wizard()

    # 3. Drift Verification & Endurance Test
    print("\n[3/3] Verifying Baseline Drift & Running endurance Test...")
    cal.analyze_drift()

    if not sim:
        print("\nStarting 5-minute automated sensor dropout check...")
        cal.run_burn_in(300) # 5m burn-in

    print("\n--- SETUP COMPLETE: Ready for Live Deployment ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", action="store_true")
    args = parser.parse_args()
    run_live_setup(args.sim)
