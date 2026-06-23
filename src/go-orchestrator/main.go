package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
)

// FCDM Python Orchestrator / Pipeline Manager Go Rewrite Skeleton
// v24.1.1 Industrial Onyx Stable

func checkHardware(simMode bool) bool {
	if simMode {
		fmt.Println("[FCDM Orchestrator] Running in Simulation Mode. Bypassing Hardware checks.")
		return true
	}

	if _, err := os.Stat("/dev/ttyACM0"); os.IsNotExist(err) {
		fmt.Println("[FCDM Orchestrator CRITICAL] Hardware not found (/dev/ttyACM0).")
		fmt.Println("To run without hardware, use the --sim flag.")
		return false
	}
	return true
}

func launchKiosk(simMode bool) {
	fmt.Println("[FCDM Orchestrator] Launching FitnessKiosk via bash script...")
	args := []string{"./scripts/fcdm_launch_production.sh"}
	if simMode {
		args = append(args, "--sim")
	}

	cmd := exec.Command("bash", args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		fmt.Printf("[FCDM Orchestrator] Kiosk exited with error: %v\n", err)
	}
}

func main() {
	simMode := flag.Bool("sim", false, "Enable simulation mode (bypasses hardware/alsa)")
	validateMode := flag.Bool("validate", false, "Run validation tests and exit")
	flag.Parse()

	if *validateMode {
		fmt.Println("[FCDM Validation] Checking pipeline integrity...")
		if !checkHardware(*simMode) {
			os.Exit(1)
		}
		fmt.Println("[FCDM Validation] Pipeline integrity verified.")
		os.Exit(0)
	}

	fmt.Println("=== Starting FCDM Orchestrator (v24.1.1) ===")
	if !checkHardware(*simMode) {
		os.Exit(1)
	}

	launchKiosk(*simMode)
}
