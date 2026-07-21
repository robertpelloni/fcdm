#!/usr/bin/env python3
"""
[DEPRECATED] FCDM Python Orchestrator
As of v24.1.1, the Python orchestrator has been deprecated in favor of the compiled Go binary.
This script serves as a passthrough for backward compatibility.
"""
import sys
import os
import subprocess

def main():
    print("[WARNING] run_pipeline.py is deprecated. Passing execution to Go fcdm-orchestrator...")

    # Resolve the absolute path to ensure execution doesn't break depending on where it's called from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    orchestrator_path = os.path.join(script_dir, "fcdm-orchestrator")

    args = [orchestrator_path, "--pipeline"]

    if "--sim" in sys.argv:
        args.append("--sim")

    try:
        subprocess.run(args, check=True, cwd=script_dir)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
