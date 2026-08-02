package hardware

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"go.bug.st/serial"
)

var (
	currentTelemetry []int
	telemetryMutex   sync.RWMutex
	serialPort       serial.Port
	isSim            bool
)

func init() {
	// Initialize with 9 empty panels
	currentTelemetry = make([]int, 9)
}

// CheckHardware verifies the presence of the FSR controller and opens the serial port
func CheckHardware(simMode bool) bool {
	fmt.Println("--- FCDM SYSTEM HEALTH CHECK (Go Native) ---")
	isSim = simMode

	if simMode {
		fmt.Println("[FCDM Orchestrator] Running in Simulation Mode. Bypassing Hardware checks.")
		go simulateTelemetry()
		return true
	}

	if _, err := os.Stat("/dev/ttyACM0"); os.IsNotExist(err) {
		fmt.Println("[WARN] /dev/ttyACM0 (Teensy) not found. Check physical connection or use --sim.")
		return false
	}

	fmt.Println("[PASS] FSR Controller (/dev/ttyACM0) detected.")

	mode := &serial.Mode{
		BaudRate: 115200,
	}
	port, err := serial.Open("/dev/ttyACM0", mode)
	if err != nil {
		fmt.Printf("[FAIL] Could not open serial port: %v\n", err)
		return false
	}
	serialPort = port

	go readSerialStream()

	return true
}

func simulateTelemetry() {
	for {
		telemetryMutex.Lock()
		currentTelemetry = []int{0, 0, 1024, 0, 50, 0, 0, 0, 4000}
		telemetryMutex.Unlock()
		time.Sleep(100 * time.Millisecond)
	}
}

func readSerialStream() {
	reader := bufio.NewReader(serialPort)
	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			fmt.Printf("[Hardware] Serial read error: %v\n", err)
			time.Sleep(1 * time.Second) // basic backoff
			continue
		}

		line = strings.TrimSpace(line)
		// Expected format: CSV of 9 integers, e.g., "0,0,1024,0,50,0,0,0,4000"
		parts := strings.Split(line, ",")
		if len(parts) == 9 {
			parsed := make([]int, 9)
			valid := true
			for i, p := range parts {
				val, err := strconv.Atoi(p)
				if err != nil {
					valid = false
					break
				}
				parsed[i] = val
			}

			if valid {
				telemetryMutex.Lock()
				currentTelemetry = parsed
				telemetryMutex.Unlock()
			}
		}
	}
}

// GetTelemetry returns the most recently read sensor states.
func GetTelemetry(simMode bool) []int {
	telemetryMutex.RLock()
	defer telemetryMutex.RUnlock()

	// Return a copy to avoid data races
	cpy := make([]int, 9)
	copy(cpy, currentTelemetry)
	return cpy
}
