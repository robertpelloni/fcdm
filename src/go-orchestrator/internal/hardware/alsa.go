package hardware

import (
	"fmt"
	"os/exec"
	"strings"
)

// SetupALSAEnvironment scans for ALSA devices and returns the optimal card index
func SetupALSAEnvironment() string {
	fmt.Println("  [INFO] Scanning for ALSA audio hardware...")
	out, err := exec.Command("aplay", "-l").Output()
	if err != nil {
		fmt.Println("[FAIL] ALSA (aplay) not found or errored.")
		return "0"
	}

	fmt.Println("[PASS] ALSA (aplay) found.")
	lines := strings.Split(string(out), "\n")
	detectedCard := ""
	priorities := []string{"Teensy", "USB", "Internal", "HDMI"}

	for _, prio := range priorities {
		for _, line := range lines {
			if strings.Contains(strings.ToLower(line), strings.ToLower(prio)) && strings.HasPrefix(line, "card") {
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
