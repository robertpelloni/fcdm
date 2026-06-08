# Hardware Integration and Industrial Construction

## 1. 9-Panel Universal Stage Construction

To build a dance platform that survives decades of high-impact fitness abuse, we use a rigid steel/aluminum chassis and FSR sensors.

### Frame and Base
- **Sub-Base**: 1/2" to 3/4" solid steel or marine plywood.
- **Grid Matrix**: 3x3 grid using 1" square structural steel tubing or 80/20 T-slot aluminum (4040 series).
- **Handbar**: 1.5" diameter stainless steel bar anchored to a heavy-gauge steel bracket.

### Panel Assembly
- **Material**: 1/2" (12mm) thick Polycarbonate (Lexan). Do NOT use acrylic.
- **Fit**: 1/16" (1.5mm) gap around the perimeter of the grid pocket.

### Sensor Stack (The Sandwich)
Inside each corner of the 9 grid pockets:
1. **Bottom**: Rigid metal frame ledge.
2. **Layer 1**: High-density neoprene rubber strip.
3. **Layer 2**: FSR Sensor (Interlink 402 or 406).
4. **Layer 3**: Rigid plastic/rubber actuator spacer disk.
5. **Top**: Polycarbonate panel.

## 2. Microcontroller Code (Teensy 4.0 / Arduino Leonardo)

The following code runs on a Teensy 4.0 at 1000Hz, providing zero-latency USB-HID input.

```cpp
#include <Keyboard.h>

const int PIN_COUNT = 9;
const int FSR_PINS[PIN_COUNT] = {A0, A1, A2, A3, A4, A5, A6, A7, A8};
const char KEY_MAPPINGS[PIN_COUNT] = {'q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c'};

int thresholds[PIN_COUNT] = {300, 300, 300, 300, 300, 300, 300, 300, 300};
bool state[PIN_COUNT] = {false};

void setup() {
  Keyboard.begin();
  // Auto-Calibration loop: Read initial resting pressure of the pad on boot
  for(int i = 0; i < PIN_COUNT; i++) {
    int baseline = analogRead(FSR_PINS[i]);
    thresholds[i] = baseline + 150; // Dynamic padding above ambient weight
  }
}

unsigned long lastCalibrationTime = 0;
const unsigned long CALIBRATION_INTERVAL = 300000; // Auto-calibrate every 5 minutes

void loop() {
  unsigned long currentTime = millis();

  // 1. Dynamic Drift Calibration
  // FSRs can drift as they heat up or as atmospheric pressure changes.
  // We periodically sample the resting state to adjust thresholds.
  if (currentTime - lastCalibrationTime > CALIBRATION_INTERVAL) {
    bool padIsIdle = true;
    for(int i=0; i<PIN_COUNT; i++) if(state[i]) padIsIdle = false;

    if (padIsIdle) {
      for(int i = 0; i < PIN_COUNT; i++) {
        int baseline = analogRead(FSR_PINS[i]);
        thresholds[i] = baseline + 150;
      }
      lastCalibrationTime = currentTime;
    }
  }

  // 2. Input Processing
  for(int i = 0; i < PIN_COUNT; i++) {
    int rawValue = analogRead(FSR_PINS[i]);

    if (rawValue > thresholds[i] && !state[i]) {
      state[i] = true;
      Keyboard.press(KEY_MAPPINGS[i]);
    } else if (rawValue < (thresholds[i] - 40) && state[i]) { // Enhanced hysteresis
      state[i] = false;
      Keyboard.release(KEY_MAPPINGS[i]);
    }
  }
  delay(1); // 1ms resolution polling
}
```

## 3. Calibration and Maintenance

### FSR Calibration Utility
To aid in setting thresholds and diagnosing sensor drift, use the provided Python utility:
```bash
PYTHONPATH=. python3 scripts/calibrate_fsr.py
```
This script connects to the Teensy serial port and provides a live feed of raw sensor values vs. current thresholds.

### Manual Threshold Adjustment
If panels are too sensitive or non-responsive:
1. Run the calibration utility.
2. Observe the `RAW` values during a "strike" vs. "idle".
3. Update the `baseline + 150` padding in the Arduino code `setup()` or the `thresholds` array in `loop()`.

## 4. Industrial Electronics and Sealing
- **Wiring**: Braided nylon sleeving inside frame channels.
- **Connectors**: Waterproof aviation plugs (GX12 or GX16).
- **Environment**: Conformal coating (silicone/acrylic) on all PCB and solder joints to prevent sweat damage.
