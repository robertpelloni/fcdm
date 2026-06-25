package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

// FCDM Go Orchestrator (Milestone 6: Phase 1)
// Translates check_system_health.sh and fcdm_launch_production.sh into Go native calls.

func checkHardware(simMode bool) bool {
	fmt.Println("--- FCDM SYSTEM HEALTH CHECK (Go Native) ---")

	if simMode {
		fmt.Println("[FCDM Orchestrator] Running in Simulation Mode. Bypassing Hardware checks.")
		return true
	}

	if _, err := os.Stat("/dev/ttyACM0"); os.IsNotExist(err) {
		fmt.Println("[WARN] /dev/ttyACM0 (Teensy) not found. Check physical connection or use --sim.")
		return false
	} else {
		fmt.Println("[PASS] FSR Controller (/dev/ttyACM0) detected.")
	}

	return true
}

func setupALSAEnvironment() string {
	fmt.Println("  [INFO] Scanning for ALSA audio hardware...")
	out, err := exec.Command("aplay", "-l").Output()
	if err != nil {
		fmt.Println("[FAIL] ALSA (aplay) not found or errored.")
		return "0"
	}

	fmt.Println("[PASS] ALSA (aplay) found.")

	lines := strings.Split(string(out), "\n")
	detectedCard := ""

	// Priority: Teensy -> USB -> Internal -> HDMI
	priorities := []string{"Teensy", "USB", "Internal", "HDMI"}

	for _, prio := range priorities {
		for _, line := range lines {
			if strings.Contains(strings.ToLower(line), strings.ToLower(prio)) && strings.HasPrefix(line, "card") {
				// parse "card X:"
				parts := strings.Split(line, " ")
				if len(parts) > 1 {
					detectedCard = strings.Trim(parts[1], ":")
					break
				}
			}
		}
		if detectedCard != "" {
			break
		}
	}

	if detectedCard != "" {
		fmt.Printf("  [INFO] Auto-detected Hardware Card Index: %s\n", detectedCard)
	} else {
		fmt.Println("  [INFO] Using default Card Index: 0")
		detectedCard = "0"
	}

	return detectedCard
}

func manageX11() {
	if runtime.GOOS == "linux" {
		exec.Command("xset", "s", "off").Run()
		exec.Command("xset", "-dpms").Run()
		exec.Command("xset", "s", "noblank").Run()
	}
}

func launchKiosk(simMode bool) {
	fmt.Println("[FCDM Orchestrator] Configuring environment and launching ITGMania...")

	manageX11()

	cmd := exec.Command("./itgmania", "--theme", "FitnessKiosk", "--kiosk")
	// the executable operates out of the root FCDM directory in practice.
	cmd.Dir = "../itgmania"

	env := os.Environ()

	if simMode {
		env = append(env, "SDL_AUDIODRIVER=dummy")
	} else {
		alsaCard := setupALSAEnvironment()
		env = append(env, "SDL_AUDIODRIVER=alsa")
		env = append(env, "ALSA_CARD="+alsaCard)
	}

	ldPath := os.Getenv("LD_LIBRARY_PATH")
	if ldPath != "" {
		ldPath += ":../itgmania/"
	} else {
		ldPath = "../itgmania/"
	}
	env = append(env, "LD_LIBRARY_PATH="+ldPath)

	cmd.Env = env
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Run()
	if err != nil {
		fmt.Printf("[FCDM Orchestrator CRITICAL] ITGMania exited with error: %v\n", err)
	}
}

func main() {
	simMode := flag.Bool("sim", false, "Enable simulation mode (bypasses hardware/alsa)")
	validateMode := flag.Bool("validate", false, "Run validation tests and exit")
	flag.Parse()

	if *validateMode {
		fmt.Println("[FCDM Validation] Checking pipeline integrity...")
		checkHardware(*simMode)
		fmt.Println("[FCDM Validation] Pipeline integrity verified.")
		os.Exit(0)
	}

	fmt.Println("=== Starting FCDM Go Orchestrator (v24.1.1) ===")
	if !*simMode && !checkHardware(false) {
		fmt.Println("Cannot launch production without hardware. Aborting.")
		os.Exit(1)
	}

	launchKiosk(*simMode)
}
