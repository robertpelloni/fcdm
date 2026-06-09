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

## 2. v2.2.0 Microcontroller Calibration Protocol

The v2.2.0 stack supports live serial tuning. Connect the Teensy/Arduino and run:
`python3 scripts/calibrate_fsr.py`

### Calibration Keys
- `t <index> <value>`: Sets the raw pressure threshold for a panel (0-1023).
- `s <index> <value>`: Sets a multiplier for sensitivity scaling (e.g. 1.2 for 20% more sensitivity).
- `w`: Writes current settings to the non-volatile memory on the controller.

## 3. Industrial Electronics and Sealing
- **Wiring**: Braided nylon sleeving inside frame channels.
- **Connectors**: Waterproof aviation plugs (GX12 or GX16).
- **Environment**: Conformal coating (silicone/acrylic) on all PCB and solder joints to prevent sweat damage.
