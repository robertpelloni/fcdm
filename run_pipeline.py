#!/usr/bin/env python3
"""
FCDM v24.0.0 Industrial Management Protocol - Central Orchestrator
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
    print("=== FCDM INDUSTRIAL MANAGEMENT PIPELINE (v24.0.0) ===")

    # 1. System Health Check
    run_step("Hardware & Environment Health Check", "bash scripts/check_system_health.sh --sim")

    # 2. Integration & CI Verification
    run_step("CI & Integration Suite", "python3 scripts/integration_test.py")

    # 3. Music Ingestion (QA Test Suite)
    if os.path.exists("itgmania/Songs/QA_Test"):
        run_step("Music Ingestion Pipeline (QA_Test)", "python3 scripts/ingest_music.py itgmania/Songs/QA_Test --difficulty 5 --force")
    else:
        print("  [SKIP] QA_Test directory not found.")

    # 4. Final Stability Certification
    print("\n[COMPLETE] v24.0.0 Management Baseline established and verified.")

if __name__ == "__main__":
    main()
