package hardware

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type FSRProfile struct {
	Thresholds  []int     `json:"thresholds"`
	Sensitivity []float64 `json:"sensitivity"`
}

var (
	profileDir    = "config/profiles"
	activeProfile = "default"
	envScriptPath = "scripts/set_fsr_env.sh"
	pins          = []string{"q", "w", "e", "a", "s", "d", "z", "x", "c"}
	CurrentProfile FSRProfile
)

func init() {
	os.MkdirAll(profileDir, 0755)
	CurrentProfile = LoadProfile(activeProfile)
}

func LoadProfile(name string) FSRProfile {
	path := filepath.Join(profileDir, fmt.Sprintf("%s.json", name))
	if _, err := os.Stat(path); err == nil {
		data, err := ioutil.ReadFile(path)
		if err == nil {
			var p FSRProfile
			if json.Unmarshal(data, &p) == nil {
				return p
			}
		}
	}

	// Default values
	return FSRProfile{
		Thresholds:  []int{450, 450, 450, 450, 450, 450, 450, 450, 450},
		Sensitivity: []float64{1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0},
	}
}

func SaveProfile() {
	path := filepath.Join(profileDir, fmt.Sprintf("%s.json", activeProfile))
	data, _ := json.MarshalIndent(CurrentProfile, "", "  ")
	ioutil.WriteFile(path, data, 0644)
}

func ExportEnv() {
	thrStrs := make([]string, 9)
	snsStrs := make([]string, 9)
	for i := 0; i < 9; i++ {
		thrStrs[i] = fmt.Sprintf("%d", CurrentProfile.Thresholds[i])
		snsStrs[i] = fmt.Sprintf("%f", CurrentProfile.Sensitivity[i])
	}

	content := fmt.Sprintf(`#!/bin/bash
# FCDM Auto-Generated Calibration Environment (v14.0.0 Go Native)

export FSR_THRESHOLDS="%s"
export FSR_SENSITIVITIES="%s"
export FCDM_ALSA_CARD="${FCDM_ALSA_CARD:-0}"

echo "FCDM: Environment Loaded (ALSA Card: $FCDM_ALSA_CARD)"
`, strings.Join(thrStrs, ","), strings.Join(snsStrs, ","))

	ioutil.WriteFile(envScriptPath, []byte(content), 0755)
	fmt.Printf("Exported environment settings to %s\n", envScriptPath)
}

func RunBurnIn(durationSec int) {
	logPath := "logs/burn_in_diagnostics.csv"
	fmt.Printf("Starting %ds Burn-In. Logging to %s\n", durationSec, logPath)
	os.MkdirAll("logs", 0755)

	file, err := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Printf("Error creating log file: %v\n", err)
		return
	}
	defer file.Close()

	stat, _ := file.Stat()
	writer := csv.NewWriter(file)
	defer writer.Flush()

	if stat.Size() == 0 {
		writer.Write([]string{"timestamp", "jitter_ms", "p0_raw", "p1_raw", "p2_raw", "p3_raw", "p4_raw", "p5_raw", "p6_raw", "p7_raw", "p8_raw"})
	}

	startTime := time.Now()
	lastPoll := startTime
	endTime := startTime.Add(time.Duration(durationSec) * time.Second)

	for time.Now().Before(endTime) {
		now := time.Now()
		jitter := float64(now.Sub(lastPoll).Milliseconds())
		lastPoll = now

		raw := GetTelemetry(isSim)
		row := []string{
			fmt.Sprintf("%f", float64(now.UnixNano())/1e9),
			fmt.Sprintf("%f", jitter),
		}
		for _, val := range raw {
			row = append(row, fmt.Sprintf("%d", val))
		}
		writer.Write(row)

		elapsed := now.Sub(startTime).Seconds()
		if int(elapsed)%10 == 0 && int(elapsed) > 0 {
			fmt.Printf("  [Burn-In] %ds elapsed...\n", int(elapsed))
		}
		time.Sleep(10 * time.Millisecond)
	}
	fmt.Println("Burn-In test complete.")
}

func RunWizard() {
	fmt.Println("--- FCDM v4.1.0 CALIBRATION WIZARD (Go Native) ---")
	fmt.Println("This wizard will guide you through physical panel strikes.")

	var newThresholds []int
	for i, p := range pins {
		fmt.Printf("\n[Step %d/9] Calibrating Panel: %s\n", i+1, strings.ToUpper(p))
		fmt.Println("Action: STRIKE and HOLD the panel now...")

		var strikeSamples []int
		for j := 0; j < 20; j++ {
			raw := GetTelemetry(isSim)
			strikeSamples = append(strikeSamples, raw[i])
			time.Sleep(50 * time.Millisecond)
		}

		strikeVal := 0
		for _, s := range strikeSamples {
			if s > strikeVal {
				strikeVal = s
			}
		}
		fmt.Printf("Detected Strike Value: %d\n", strikeVal)

		fmt.Println("Action: RELEASE the panel...")
		time.Sleep(1 * time.Second)

		var idleSamples []int
		for j := 0; j < 20; j++ {
			raw := GetTelemetry(isSim)
			idleSamples = append(idleSamples, raw[i])
			time.Sleep(50 * time.Millisecond)
		}

		idleSum := 0
		for _, s := range idleSamples {
			idleSum += s
		}
		idleVal := float64(idleSum) / float64(len(idleSamples))
		fmt.Printf("Detected Idle Value: %.2f\n", idleVal)

		thr := int(idleVal + (float64(strikeVal)-idleVal)*0.4)
		fmt.Printf("Setting %s Threshold: %d\n", strings.ToUpper(p), thr)
		newThresholds = append(newThresholds, thr)
	}

	CurrentProfile.Thresholds = newThresholds
	SaveProfile()
	fmt.Println("\n[SUCCESS] Calibration Profile Updated.")
	ExportEnv()
}

func RunCalibrationDisplay() {
	fmt.Println("FCDM FSR Utility (v10.0.0 Go Native) - Mode: CALIB")
	for {
		rawValues := GetTelemetry(isSim)

		if !isSim {
			fmt.Print("\033[H\033[2J") // clear screen
		}

		fmt.Println("--- FCDM CALIBRATION ---")
		fmt.Println("P | RAW | THR | STATUS")
		fmt.Println("--|-----|-----|-------")
		for i, p := range pins {
			raw := rawValues[i]
			thr := CurrentProfile.Thresholds[i]
			status := "IDLE"
			if raw > thr {
				status = "STRIKE"
			}
			fmt.Printf("%s | %03d | %03d | %s\n", strings.ToUpper(p), raw, thr, status)
		}

		if isSim {
			break
		}
		time.Sleep(100 * time.Millisecond)
	}
}
