# FCDM Hardware Architecture & Wiring Guide

## Overview
The Fitness Center Dance Machine (FCDM) relies on a custom 9-panel matrix platform, designed for heavy industrial use. The primary microcontroller is a **Teensy 4.0**, due to its exceptionally low latency USB polling and native hardware keyboard emulation capabilities.

## Sensor Stack (Force Sensing Resistors)
We utilize high-durability FSR sensors.
- **Placement**: Each of the 9 panels is supported by 4 corner FSRs.
- **Logic**: The 4 sensors for a given panel are wired in parallel to act as a single variable resistor.

## Teensy 4.0 Wiring Diagram

| Panel Direction | Teensy Pin | Key Mapping |
|-----------------|------------|-------------|
| Up-Left (UL)    | Pin 0      | Q           |
| Up (U)          | Pin 1      | W           |
| Up-Right (UR)   | Pin 2      | E           |
| Left (L)        | Pin 3      | A           |
| Center (C)      | Pin 4      | S           |
| Right (R)       | Pin 5      | D           |
| Down-Left (DL)  | Pin 6      | Z           |
| Down (D)        | Pin 7      | X           |
| Down-Right (DR) | Pin 8      | C           |

*Ground loops*: All FSR circuits return to the common Ground (GND) pin on the Teensy.
*Pull-up/Pull-down*: We utilize the Teensy's internal pull-up resistors (`INPUT_PULLUP`). The FSR completes the circuit to ground when compressed.

## ALSA & Audio Priority
FCDM avoids PulseAudio/PipeWire.
Ensure ALSA sees the primary DAC at `hw:0,0`.
Check priority via: `cat /proc/asound/modules`
