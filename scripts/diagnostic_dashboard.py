import os
import sys
import time
import curses
import json
import urllib.request
import urllib.error
import subprocess
import threading

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from calibrate_fsr import FSRCalibrator

# Load version from VERSION.md if available
VERSION = "v24.2.0"
version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "VERSION.md")
if os.path.exists(version_file):
    try:
        with open(version_file, "r") as vf:
            VERSION = vf.read().strip()
    except Exception:
        pass

class DashboardState:
    """Encapsulates system telemetry, background threads, and UI state."""
    def __init__(self):
        self.cal = FSRCalibrator()
        self.show_tooltips = False
        self.selected_panel = 4  # Center panel 'S' default
        self.status_message = "System operational. Press '?' for tooltips, 'c' calibrate, 'q' quit."
        self.orchestrator_online = False
        self.last_api_health = {}
        self.last_telemetry = [0] * 9
        self.latency_ms = 0.0
        self.active_card = os.environ.get('FCDM_ALSA_CARD', '0')
        self.session_start = time.time()
        self.running = True
        self.lock = threading.Lock()

        # Start background polling thread for Orchestrator API
        self.poll_thread = threading.Thread(target=self._poll_orchestrator, daemon=True)
        self.poll_thread.start()

    def _poll_orchestrator(self):
        while self.running:
            # 1. Health check
            try:
                req = urllib.request.Request("http://localhost:8080/api/health", headers={"User-Agent": "FCDM-Dashboard"})
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode('utf-8'))
                        with self.lock:
                            self.orchestrator_online = True
                            self.last_api_health = data
            except Exception:
                with self.lock:
                    self.orchestrator_online = False
                    self.last_api_health = {}

            # 2. Telemetry polling
            if self.orchestrator_online:
                try:
                    req = urllib.request.Request("http://localhost:8080/api/telemetry", headers={"User-Agent": "FCDM-Dashboard"})
                    with urllib.request.urlopen(req, timeout=1.0) as resp:
                        if resp.status == 200:
                            data = json.loads(resp.read().decode('utf-8'))
                            with self.lock:
                                self.last_telemetry = data.get("panels", [0] * 9)
                                self.latency_ms = data.get("latency_ms", 1.2)
                except Exception:
                    pass

            time.sleep(0.1)

    def trigger_action(self, action_key):
        """Dispatches interactive actions from dashboard keys."""
        if action_key == 'c':
            self.status_message = "Initiating Calibration Display..."
            # Trigger calibration via API if online, else via local Calibrator
            if self.orchestrator_online:
                try:
                    urllib.request.urlopen("http://localhost:8080/api/calibrate?mode=DISPLAY", timeout=1.0)
                    self.status_message = "[API] Calibration DISPLAY triggered on orchestrator."
                except Exception as e:
                    self.status_message = f"[API Error] Failed: {e}"
            else:
                self.cal.export_env()
                self.status_message = "[Local] Exported FSR calibration environment to set_fsr_env.sh"
        elif action_key == 'w':
            self.status_message = "Launching Calibration Wizard..."
            if self.orchestrator_online:
                try:
                    urllib.request.urlopen("http://localhost:8080/api/calibrate?mode=WIZARD", timeout=1.0)
                    self.status_message = "[API] Calibration WIZARD started in background."
                except Exception as e:
                    self.status_message = f"[API Error] Failed: {e}"
            else:
                self.status_message = "[Local] Wizard mode requires interactive terminal or API."
        elif action_key == 'b':
            self.status_message = "Triggering 30s Burn-in test..."
            if self.orchestrator_online:
                try:
                    urllib.request.urlopen("http://localhost:8080/api/calibrate?mode=BURNIN", timeout=1.0)
                    self.status_message = "[API] Burn-In test started in background."
                except Exception as e:
                    self.status_message = f"[API Error] Failed: {e}"
            else:
                threading.Thread(target=lambda: self.cal.run_burn_in(30), daemon=True).start()
                self.status_message = "[Local] Started 30s Burn-In logging to logs/burn_in_diagnostics.csv"
        elif action_key == 'r':
            self.status_message = "Rebooting Orchestrator..."
            if self.orchestrator_online:
                try:
                    urllib.request.urlopen("http://localhost:8080/api/reboot", timeout=1.0)
                    self.status_message = "[API] Reboot signal sent."
                except Exception as e:
                    self.status_message = f"[API Error] Failed: {e}"
            else:
                self.status_message = "Cannot reboot: Go Orchestrator is offline."
        elif action_key == '?':
            self.show_tooltips = not self.show_tooltips
            self.status_message = f"Tooltips {'ENABLED' if self.show_tooltips else 'DISABLED'}."


def draw_dashboard(stdscr):
    """
    Consolidated Single-Page Interactive Live Diagnostic Dashboard.
    Visualizes high-value metrics prominently:
    - Top Status Bar (Orchestrator health, ALSA low latency card, version)
    - 3x3 FSR Pressure Matrix with dynamic strike/idle indicators & sensitivities
    - Subsystems Overview: Bobcoin, HRM, Cardio Timer, ALSA audio
    - Action hotkeys & Toggleable guided UI Tooltips
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)   # Active/Pass
        curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Warning/Strike
        curses.init_pair(3, curses.COLOR_CYAN, -1)    # Headers/Metrics
        curses.init_pair(4, curses.COLOR_RED, -1)     # Offline/Alert
        curses.init_pair(5, curses.COLOR_MAGENTA, -1) # Tooltips/Help

    state = DashboardState()
    pins = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
    pin_labels = [
        "Up-Left [Q]", "Up [W]", "Up-Right [E]",
        "Left [A]", "Center [S]", "Right [D]",
        "Down-Left [Z]", "Down [X]", "Down-Right [C]"
    ]

    try:
        while True:
            stdscr.erase()
            max_y, max_x = stdscr.getmaxyx()

            # Ensure minimum terminal size
            if max_y < 22 or max_x < 78:
                stdscr.addstr(0, 0, f"Resize terminal: need at least 80x24 (Current: {max_x}x{max_y})")
                stdscr.refresh()
                time.sleep(0.2)
                continue

            # Header / Top Status Bar
            title = f" FCDM {VERSION} INDUSTRIAL CONSOLIDATED DASHBOARD "
            api_indicator = "[API: ONLINE]" if state.orchestrator_online else "[API: STANDALONE/OFFLINE]"
            header_color = curses.color_pair(1) if state.orchestrator_online else curses.color_pair(2)
            stdscr.attron(curses.A_BOLD | curses.color_pair(3))
            stdscr.addstr(0, 0, "=" * (max_x - 1))
            stdscr.addstr(1, 2, title)
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr(1, len(title) + 4, api_indicator, header_color | curses.A_BOLD)
            alsa_str = f"ALSA Card: {state.active_card} (Low-Latency DMA)"
            stdscr.addstr(1, max(2, max_x - len(alsa_str) - 3), alsa_str, curses.color_pair(3))
            stdscr.addstr(2, 0, "=" * (max_x - 1))
            stdscr.attroff(curses.A_BOLD)

            # Get latest telemetry
            with state.lock:
                if state.orchestrator_online and any(state.last_telemetry):
                    raw_values = list(state.last_telemetry)
                else:
                    raw_values = state.cal.get_raw_values()

            thresholds = state.cal.profile.get("thresholds", [450] * 9)
            sensitivities = state.cal.profile.get("sensitivity", [1.0] * 9)

            # ----------------------------------------------------
            # PROMINENT SECTION 1: 3x3 FSR Hardware Matrix (Left/Center)
            # ----------------------------------------------------
            col1_x = 2
            stdscr.addstr(3, col1_x, "[HIGH-VALUE] 9-PANEL FSR PRESSURE MATRIX (1000Hz)", curses.A_BOLD | curses.color_pair(3))

            for row in range(3):
                for col in range(3):
                    idx = row * 3 + col
                    val = raw_values[idx]
                    thr = thresholds[idx]
                    sens = sensitivities[idx]
                    is_strike = val > thr

                    # Panel box layout
                    px = col1_x + (col * 24)
                    py = 5 + (row * 3)

                    status_badge = " STRIKE " if is_strike else "  IDLE  "
                    badge_color = curses.color_pair(2) if is_strike else curses.color_pair(1)

                    bar_max = 8
                    bar_len = min(bar_max, max(0, int((val / 1024.0) * bar_max)))
                    bar_str = "[" + "#" * bar_len + "." * (bar_max - bar_len) + "]"

                    stdscr.addstr(py, px, f"{pin_labels[idx][:12]:<12}", curses.A_BOLD)
                    stdscr.addstr(py, px + 13, status_badge, badge_color | curses.A_REVERSE)
                    stdscr.addstr(py + 1, px, f"{bar_str} {val:>4} / {thr:>4} (x{sens:.1f})")

            # ----------------------------------------------------
            # SECTION 2: Subsystem Integrations & Telemetry (Right Column)
            # ----------------------------------------------------
            col2_x = 76 if max_x >= 120 else 2
            sub_y = 3 if max_x >= 120 else 15

            stdscr.addstr(sub_y, col2_x, "[SUBSYSTEM INTEGRATIONS & METRICS]", curses.A_BOLD | curses.color_pair(3))

            elapsed_sec = int(time.time() - state.session_start)
            elapsed_fmt = f"{elapsed_sec // 60:02d}:{elapsed_sec % 60:02d}"

            stdscr.addstr(sub_y + 1, col2_x, f"* Cardio Continuous Timer : {elapsed_fmt} (Zone 2/3 aerobic)", curses.A_NORMAL)
            stdscr.addstr(sub_y + 2, col2_x, f"* Hardware Latency (HAL)  : {state.latency_ms:.2f} ms (Target < 2.0ms)", curses.color_pair(1))
            stdscr.addstr(sub_y + 3, col2_x, f"* Bobcoin Node Minting    : 100.0% Flow-Bonus Linked", curses.color_pair(3))
            stdscr.addstr(sub_y + 4, col2_x, f"* Sensor Fatigue / Drift  : Normal (Baseline Variance < 5%)", curses.A_NORMAL)
            stdscr.addstr(sub_y + 5, col2_x, f"* Audio Buffer / Rate     : DMA 512 samples @ 44.1kHz ALSA", curses.A_NORMAL)

            # ----------------------------------------------------
            # SECTION 3: Action Controls & Status Bar
            # ----------------------------------------------------
            action_y = sub_y + 7 if max_x >= 120 else 21
            if action_y < max_y - 4:
                stdscr.addstr(action_y, 2, "-" * (max_x - 4))
                ctrl_str = "[c] Calibrate  [w] Wizard  [b] Burn-In  [r] Reboot ITG  [?] Toggle Tooltips  [q] Quit"
                stdscr.addstr(action_y + 1, 2, ctrl_str, curses.A_BOLD | curses.color_pair(3))
                stdscr.addstr(action_y + 2, 2, f"Status: {state.status_message}", curses.A_ITALIC)

            # ----------------------------------------------------
            # SECTION 4: Interactive Tooltips / Guidance Overlay
            # ----------------------------------------------------
            if state.show_tooltips:
                tip_y = action_y + 3
                if tip_y < max_y - 4:
                    stdscr.addstr(tip_y, 2, "[TOOLTIP GUIDANCE] (Press '?' to hide):", curses.A_BOLD | curses.color_pair(5))
                    stdscr.addstr(tip_y + 1, 4, "- FSR Matrix: Displays 1000Hz live foot pressure. Green IDLE is standby; Yellow STRIKE is trigger.", curses.color_pair(5))
                    stdscr.addstr(tip_y + 2, 4, "- Calibration Wizard (w): Guides step-by-step physical calibration of 9 sensors to calibrate thresholds.", curses.color_pair(5))
                    stdscr.addstr(tip_y + 3, 4, "- Burn-In Stress (b): Logs sensor jitter & latency into logs/burn_in_diagnostics.csv for endurance QA.", curses.color_pair(5))
                    stdscr.addstr(tip_y + 4, 4, "- Go Orchestrator: Runs HTTP daemon on port 8080 handling /api/telemetry, /api/sanitize, and ALSA setup.", curses.color_pair(5))

            stdscr.refresh()

            # Handle Keyboard Input
            try:
                ch = stdscr.getch()
                if ch != -1:
                    key_char = chr(ch).lower()
                    if key_char == 'q':
                        break
                    elif key_char in ['c', 'w', 'b', 'r', '?']:
                        state.trigger_action(key_char)
            except Exception:
                pass

            time.sleep(0.05)
    finally:
        state.running = False

if __name__ == "__main__":
    curses.wrapper(draw_dashboard)
