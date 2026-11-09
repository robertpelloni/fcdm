#!/bin/bash
# FCDM v24.2.0 Production Stress Runner
# Orchestrates stress testing using the native Go orchestrator and generates QA certification.

echo "--- FCDM v24.2.0 PRODUCTION STRESS RUNNER ---"

DURATION=${1:-60}

# 1. Initialization
bash scripts/check_system_health.sh --sim

# 2. Native Stress Session via Go Orchestrator
echo "Starting ${DURATION}s stress session..."
if [ -f "./fcdm-orchestrator" ]; then
    ./fcdm-orchestrator --sim --stress-test --duration "$DURATION"
else
    ./src/go-orchestrator/go-orchestrator --sim --stress-test --duration "$DURATION"
fi

# 3. Generate QA Report
echo "Generating Industrial QA Report..."
python3 scripts/industrial_qa_report.py logs/stress_results.csv

echo "--- SESSION COMPLETE ---"
