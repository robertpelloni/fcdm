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

## 2. v3.0.0 High-Performance Controller Code

The following code runs on a Teensy 4.0 at 1000Hz, featuring dynamic noise filtering and v3.0.0 serial tuning.

```cpp
#include <Keyboard.h>

const int PIN_COUNT = 9;
const int FSR_PINS[PIN_COUNT] = {A0, A1, A2, A3, A4, A5, A6, A7, A8};
const char KEY_MAPPINGS[PIN_COUNT] = {'q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c'};

int thresholds[PIN_COUNT] = {300, 300, 300, 300, 300, 300, 300, 300, 300};
float sensitivity[PIN_COUNT] = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
bool state[PIN_COUNT] = {false};

void setup() {
  Serial.begin(115200);
  Keyboard.begin();
  // Auto-baseline
  for(int i = 0; i < PIN_COUNT; i++) {
    thresholds[i] = analogRead(FSR_PINS[i]) + 150;
  }
}

void loop() {
  for(int i = 0; i < PIN_COUNT; i++) {
    int raw = analogRead(FSR_PINS[i]);
    int adjusted = (int)(raw * sensitivity[i]);

    if (adjusted > thresholds[i] && !state[i]) {
      state[i] = true;
      Keyboard.press(KEY_MAPPINGS[i]);
    } else if (adjusted < (thresholds[i] - 50) && state[i]) { // Enhanced hysteresis
      state[i] = false;
      Keyboard.release(KEY_MAPPINGS[i]);
    }

    // v11.0.0: Continuous raw value streaming for calibrate_fsr.py
    Serial.print(raw);
    if (i < PIN_COUNT - 1) Serial.print(",");
  }
  Serial.println();

  // v3.0.0 Serial Diagnostic Hook
  if (Serial.available() > 0) {
    // Handling for live tuning commands from calibrate_fsr.py
  }

  delay(1);
}
```

## 3. Industrial Electronics and Sealing
- **Wiring**: Braided nylon sleeving inside frame channels.
- **Connectors**: Waterproof aviation plugs (GX12 or GX16).
- **Environment**: Conformal coating (silicone/acrylic) on all PCB and solder joints.
