#!/usr/bin/env python3
"""
FCDM v24.1.1 Industrial Management Protocol - Central Orchestrator
Automates music ingestion, hardware health checks, and CI verification.
"""
import os
import sys
import subprocess

def run_step(name, command):
    print(f"\n>>> EXECUTING: {name} ...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"--- SUCCESS: {name} ---")
    except subprocess.CalledProcessError as e:
        print(f"!!! FAILED: {name} (Exit: {e.returncode}) !!!")
        sys.exit(1)

def main():
    print("=== FCDM INDUSTRIAL MANAGEMENT PIPELINE (v24.1.1) ===")
    run_step("Hardware & Environment Health Check", "bash scripts/check_system_health.sh --sim")
    run_step("CI & Integration Suite", "PYTHONPATH=. python3 scripts/integration_test.py")

    # Optional stream sanitization loop verification if a test audio is present
    if os.path.exists("test_audio.wav"):
        run_step("Core Generation Loop Validation", "PYTHONPATH=. python3 scripts/core_loop.py test_audio.wav --output_dir itgmania/Songs/FCDM_Autogen")
    elif os.path.exists("itgmania/Songs/QA_Test"):
        run_step("Music Ingestion Pipeline (QA_Test)", "python3 scripts/ingest_music.py itgmania/Songs/QA_Test --difficulty 5 --force")

    print("\n[COMPLETE] v24.1.1 Management Baseline established and verified.")

if __name__ == "__main__":
    main()
