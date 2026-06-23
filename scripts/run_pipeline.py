#!/usr/bin/env python3
"""
FCDM Python Orchestrator / Pipeline Manager
v24.1.1 Industrial Onyx Stable
"""

import sys
import subprocess
import argparse
import time

def check_hardware(sim_mode=False):
    if sim_mode:
        print("[FCDM Orchestrator] Running in Simulation Mode. Bypassing Hardware checks.")
        return True

    try:
        import os
        if not os.path.exists("/dev/ttyACM0"):
            print("[FCDM Orchestrator CRITICAL] Hardware not found (/dev/ttyACM0).")
            print("To run without hardware, use the --sim flag.")
            return False
        return True
    except Exception as e:
        print(f"Hardware check failed: {e}")
        return False

def launch_kiosk(sim_mode=False):
    print("[FCDM Orchestrator] Launching FitnessKiosk via bash script...")
    args = ["./scripts/fcdm_launch_production.sh"]
    if sim_mode:
        args.append("--sim")

    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[FCDM Orchestrator] Kiosk exited with error: {e}")

def main():
    parser = argparse.ArgumentParser(description="FCDM Pipeline Manager")
    parser.add_argument("--sim", action="store_true", help="Enable simulation mode (bypasses hardware/alsa)")
    parser.add_argument("--validate", action="store_true", help="Run validation tests and exit")
    args = parser.parse_args()

    if args.validate:
        print("[FCDM Validation] Checking pipeline integrity...")
        if not check_hardware(sim_mode=args.sim):
            sys.exit(1)
        print("[FCDM Validation] Pipeline integrity verified.")
        sys.exit(0)

    print("=== Starting FCDM Orchestrator (v24.1.1) ===")
    if not check_hardware(args.sim):
        sys.exit(1)

    launch_kiosk(args.sim)

if __name__ == "__main__":
    main()
