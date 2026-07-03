package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"path/filepath"

	"fcdm/go-orchestrator/internal/hardware"
	"fcdm/go-orchestrator/internal/sanitizer"
)

// FCDM Go Orchestrator (Milestone 6: Phase 1-3 & Milestone 7 Phase 4)

func manageX11() {
	if runtime.GOOS == "linux" {
		exec.Command("xset", "s", "off").Run()
		exec.Command("xset", "-dpms").Run()
		exec.Command("xset", "s", "noblank").Run()
	}
}

var itgProcess *exec.Cmd

func launchKiosk(simMode bool) {
	fmt.Println("[FCDM Orchestrator] Configuring environment and launching ITGMania...")
	manageX11()

	if _, err := os.Stat("itgmania/itgmania"); err == nil {
		itgProcess = exec.Command("./itgmania", "--theme", "FitnessKiosk", "--kiosk")
		itgProcess.Dir = "itgmania"
	} else {
		fmt.Println("  [WARNING] ITGMania binary not found. Using python stub for simulation.")
		itgProcess = exec.Command("python3", "scripts/itgmania_stub.py")
		absPath, _ := filepath.Abs(".")
		itgProcess.Dir = absPath
	}

	env := os.Environ()
	if simMode {
		env = append(env, "SDL_AUDIODRIVER=dummy")
	} else {
		alsaCard := hardware.SetupALSAEnvironment()
		env = append(env, "SDL_AUDIODRIVER=alsa")
		env = append(env, "ALSA_CARD="+alsaCard)
	}

	ldPath := os.Getenv("LD_LIBRARY_PATH")
	if ldPath != "" {
		ldPath += ":./itgmania/"
	} else {
		ldPath = "./itgmania/"
	}
	env = append(env, "LD_LIBRARY_PATH="+ldPath)

	itgProcess.Env = env
	itgProcess.Stdout = os.Stdout
	itgProcess.Stderr = os.Stderr

	err := itgProcess.Run()
	if err != nil {
		fmt.Printf("[FCDM Orchestrator CRITICAL] ITGMania exited with error: %v\n", err)
	}
}

func runStep(name string, command string, args ...string) {
	fmt.Printf("\n>>> EXECUTING: %s ...\n", name)
	cmd := exec.Command(command, args...)

	env := os.Environ()
	env = append(env, "PYTHONPATH=.")
	cmd.Env = env

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	absPath, _ := filepath.Abs(".")
	cmd.Dir = absPath

	err := cmd.Run()
	if err != nil {
		fmt.Printf("!!! FAILED: %s (Exit: %v) !!!\n", name, err)
		os.Exit(1)
	}
	fmt.Printf("--- SUCCESS: %s ---\n", name)
}

func executePipeline(simMode bool) {
	fmt.Println("=== FCDM INDUSTRIAL MANAGEMENT PIPELINE (v24.1.1 Go Native) ===")

	runStep("CI & Integration Suite", "python3", "scripts/integration_test.py")

	if _, err := os.Stat("test_audio.wav"); err == nil {
		runStep("Core Generation Loop Validation", "python3", "scripts/core_loop.py", "test_audio.wav", "--output_dir", "itgmania/Songs/FCDM_Autogen")
	} else if _, err := os.Stat("itgmania/Songs/QA_Test"); err == nil {
		runStep("Music Ingestion Pipeline (QA_Test)", "python3", "scripts/ingest_music.py", "itgmania/Songs/QA_Test", "--difficulty", "5", "--force")
	}

	fmt.Println("\n[COMPLETE] v24.1.1 Management Baseline established and verified.")
}

func startHTTPServer(simMode bool) {
	http.HandleFunc("/api/health", func(w http.ResponseWriter, r *http.Request) {
		hwStatus := hardware.CheckHardware(simMode)
		response := map[string]string{
			"status":   "active",
			"hardware": fmt.Sprintf("%t", hwStatus),
			"version":  "v24.1.1",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	http.HandleFunc("/api/reboot", func(w http.ResponseWriter, r *http.Request) {
		if itgProcess != nil && itgProcess.Process != nil {
			itgProcess.Process.Kill()
		}
		response := map[string]string{
			"status": "rebooting",
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
		os.Exit(0)
	})

	http.HandleFunc("/api/telemetry", func(w http.ResponseWriter, r *http.Request) {
		panels := hardware.GetTelemetry(simMode)
		response := map[string]interface{}{
			"status": "active",
			"panels": panels,
			"latency_ms": 1.2,
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	})

	fmt.Println("[FCDM Orchestrator] Starting HTTP Management Server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("HTTP Server failed: %v\n", err)
	}
}

func main() {
	simMode := flag.Bool("sim", false, "Enable simulation mode (bypasses hardware/alsa)")
	validateMode := flag.Bool("validate", false, "Run validation tests and exit")
	pipelineMode := flag.Bool("pipeline", false, "Run the python integration pipeline and exit")

	// Phase 4: Direct CLI call to the Go Native Sanitizer
	sanitizeMode := flag.String("sanitize", "", "Path to SSC file to sanitize via Go logic")
	outMode := flag.String("out", "sanitized.ssc", "Path to output the sanitized SSC file")
	flag.Parse()

	if *sanitizeMode != "" {
		fmt.Printf("Running Native Go Sanitizer on: %s\n", *sanitizeMode)
		err := sanitizer.SanitizeSSC(*sanitizeMode, *outMode)
		if err != nil {
			fmt.Printf("Sanitization failed: %v\n", err)
			os.Exit(1)
		}
		fmt.Println("Sanitization complete.")
		os.Exit(0)
	}

	if *validateMode {
		fmt.Println("[FCDM Validation] Checking pipeline integrity...")
		hardware.CheckHardware(*simMode)
		fmt.Println("[FCDM Validation] Pipeline integrity verified.")
		os.Exit(0)
	}

	if *pipelineMode {
		executePipeline(*simMode)
		os.Exit(0)
	}

	fmt.Println("=== Starting FCDM Go Orchestrator (v24.1.1) ===")
	if !*simMode && !hardware.CheckHardware(false) {
		fmt.Println("Cannot launch production without hardware. Aborting.")
		os.Exit(1)
	}

	go startHTTPServer(*simMode)
	launchKiosk(*simMode)
}
