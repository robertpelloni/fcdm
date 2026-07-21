import os
import sys
import time
import curses
import numpy as np

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

def draw_dashboard(stdscr):
    """
    v17.0.0 Live Diagnostic Dashboard.
    Visualizes FSR pressure and system stability in real-time.
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    cal = FSRCalibrator()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "--- FCDM v17.0.0 LIVE DIAGNOSTIC DASHBOARD ---", curses.A_BOLD)

        raw_values = cal.get_raw_values()

        # 1. Visualize Panels (3x3 grid)
        stdscr.addstr(2, 0, "PANEL PRESSURE MATRIX:")
        pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        for row in range(3):
            for col in range(3):
                idx = row * 3 + col
                val = raw_values[idx]
                # Simple bar
                bar_len = int(val / 100)
                stdscr.addstr(4 + row, col * 20, f"{pins[idx].upper()}: [{'#' * bar_len}{' ' * (10 - bar_len)}] {val}")

        # 2. System Status
        stdscr.addstr(9, 0, "SYSTEM HEALTH:")
        stdscr.addstr(10, 2, f"FSR Polling: ACTIVE (1000Hz simulated)")
        stdscr.addstr(11, 2, f"ALSA Card: {os.environ.get('FCDM_ALSA_CARD', '0')}")

        stdscr.addstr(14, 0, "Press 'q' to exit.")
        stdscr.refresh()

        # Handle Exit
        try:
            key = stdscr.getkey()
            if key == 'q': break
        except Exception:
            pass

        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(draw_dashboard)
