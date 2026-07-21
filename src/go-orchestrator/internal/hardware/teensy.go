package hardware

import (
	"fmt"
	"os"
)

// CheckHardware verifies the presence of the FSR controller
func CheckHardware(simMode bool) bool {
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

// GetTelemetry returns current sensor states. In a full implementation, this reads from /dev/ttyACM0.
func GetTelemetry(simMode bool) []int {
	if simMode {
		return []int{0, 0, 1024, 0, 50, 0, 0, 0, 4000} // Mock values for simulation
	}

	// Real implementation would open the serial port and read the latest parsed line
	// For now, we return mock data since we aren't using a third-party serial library yet
	return []int{0, 0, 0, 0, 0, 0, 0, 0, 0}
}
