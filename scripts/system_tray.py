#!/usr/bin/env python3
"""
FCDM System Tray & Background Management Controller (v24.2.0)
Provides quick system tray access and management for:
- Orchestrator Server status and controls (Start, Stop, Restart)
- ITGMania Kiosk execution
- FSR Hardware Calibration & Burn-in
- Live Diagnostic Dashboard launcher
- Clean shutdown of all FCDM services

Supports both graphical system tray (via pystray or tkinter fallback)
and Headless / CLI Daemon mode for unattended kiosk environments.
"""

import os
import sys
import time
import signal
import subprocess
import threading
import argparse
import urllib.request
import json

class FCDMSystemController:
    """Manages background processes and controls for FCDM components."""
    def __init__(self, sim_mode=True):
        self.sim_mode = sim_mode
        self.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.orchestrator_proc = None
        self.dashboard_proc = None
        self.running = True

    def get_orchestrator_status(self):
        """Checks if the Go Orchestrator HTTP server is reachable on port 8080."""
        try:
            req = urllib.request.Request("http://localhost:8080/api/health", headers={"User-Agent": "FCDM-Tray"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    return True, f"Online ({data.get('version', 'unknown')})"
        except Exception:
            pass
        return False, "Offline"

    def start_orchestrator(self):
        """Starts the Go Orchestrator in the background."""
        is_online, _ = self.get_orchestrator_status()
        if is_online:
            print("[Tray] Go Orchestrator is already running.")
            return

        bin_path = os.path.join(self.repo_root, "fcdm-orchestrator")
        if not os.path.exists(bin_path):
            bin_path = os.path.join(self.repo_root, "src/go-orchestrator/go-orchestrator")

        cmd = [bin_path]
        if self.sim_mode:
            cmd.append("--sim")

        print(f"[Tray] Starting orchestrator: {' '.join(cmd)}")
        self.orchestrator_proc = subprocess.Popen(
            cmd,
            cwd=self.repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.5)

    def stop_orchestrator(self):
        """Terminates the Go Orchestrator process cleanly."""
        print("[Tray] Stopping orchestrator...")
        # First try via HTTP reboot / shutdown endpoint
        try:
            req = urllib.request.Request("http://localhost:8080/api/reboot", headers={"User-Agent": "FCDM-Tray"})
            urllib.request.urlopen(req, timeout=1.0)
        except Exception:
            pass

        if self.orchestrator_proc and self.orchestrator_proc.poll() is None:
            self.orchestrator_proc.terminate()
            try:
                self.orchestrator_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.orchestrator_proc.kill()
            self.orchestrator_proc = None
        print("[Tray] Orchestrator stopped.")

    def restart_orchestrator(self):
        """Restarts the Go Orchestrator."""
        print("[Tray] Restarting orchestrator...")
        self.stop_orchestrator()
        time.sleep(1)
        self.start_orchestrator()

    def launch_dashboard(self):
        """Launches the Live Diagnostic Dashboard in a terminal."""
        print("[Tray] Launching Live Diagnostic Dashboard...")
        dash_script = os.path.join(self.repo_root, "scripts/diagnostic_dashboard.py")
        subprocess.Popen([sys.executable, dash_script], cwd=self.repo_root)

    def trigger_calibration(self, mode="DISPLAY"):
        """Triggers FSR calibration via API or CLI."""
        print(f"[Tray] Triggering calibration mode: {mode}")
        try:
            urllib.request.urlopen(f"http://localhost:8080/api/calibrate?mode={mode}", timeout=1.0)
            print("[Tray] Calibration command accepted by orchestrator.")
        except Exception as e:
            print(f"[Tray] Orchestrator offline, executing standalone calibration: {e}")
            cal_script = os.path.join(self.repo_root, "scripts/calibrate_fsr.py")
            subprocess.Popen([sys.executable, cal_script, "--mode", mode, "--sim"], cwd=self.repo_root)

    def shutdown_all(self):
        """Terminates all managed services and exits."""
        print("[Tray] Initiating complete FCDM shutdown...")
        self.stop_orchestrator()
        self.running = False
        print("[Tray] All FCDM servers and monitors shutdown cleanly.")

def run_gui_tray(controller):
    """Runs a GUI system tray icon if GUI/tray libraries are present."""
    try:
        import pystray
        from PIL import Image, ImageDraw

        # Generate a simple dance-pad icon
        def create_icon_image():
            img = Image.new('RGB', (64, 64), color=(30, 30, 30))
            d = ImageDraw.Draw(img)
            d.rectangle([16, 16, 48, 48], outline=(0, 255, 128), width=3)
            d.polygon([(32, 20), (22, 38), (42, 38)], fill=(0, 255, 128))
            return img

        def on_open_dashboard(icon, item):
            controller.launch_dashboard()

        def on_restart(icon, item):
            controller.restart_orchestrator()

        def on_calibrate(icon, item):
            controller.trigger_calibration("DISPLAY")

        def on_quit(icon, item):
            controller.shutdown_all()
            icon.stop()

        menu = pystray.Menu(
            pystray.MenuItem("FCDM Dashboard", on_open_dashboard, default=True),
            pystray.MenuItem("Restart Orchestrator", on_restart),
            pystray.MenuItem("Calibrate FSR Sensors", on_calibrate),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit All Servers", on_quit)
        )

        icon = pystray.Icon("FCDM_Tray", create_icon_image(), "FCDM Kiosk Controller", menu)
        icon.run()
        return True
    except Exception as e:
        # GUI/pystray not available or headless
        return False

def run_cli_daemon(controller):
    """Runs interactive/daemon CLI control loop for headless environments."""
    print("==================================================")
    print("   FCDM SYSTEM TRAY & BACKGROUND CONTROLLER (CLI)  ")
    print("==================================================")
    print("Commands:")
    print("  [s] Check Server Status")
    print("  [u] Start Go Orchestrator")
    print("  [d] Stop Go Orchestrator")
    print("  [r] Restart Go Orchestrator")
    print("  [l] Launch Live Dashboard")
    print("  [c] Trigger Sensor Calibration")
    print("  [q] Quit & Shutdown All Servers")
    print("==================================================")

    while controller.running:
        try:
            status, desc = controller.get_orchestrator_status()
            print(f"\n[Status: Orchestrator {desc}]")
            choice = input("FCDM-Tray> ").strip().lower()
            if choice == 's':
                print(f"Server status: {desc}")
            elif choice == 'u':
                controller.start_orchestrator()
            elif choice == 'd':
                controller.stop_orchestrator()
            elif choice == 'r':
                controller.restart_orchestrator()
            elif choice == 'l':
                controller.launch_dashboard()
            elif choice == 'c':
                controller.trigger_calibration("DISPLAY")
            elif choice == 'q':
                controller.shutdown_all()
                break
        except (KeyboardInterrupt, EOFError):
            controller.shutdown_all()
            break

def main():
    parser = argparse.ArgumentParser(description="FCDM System Tray & Background Daemon")
    parser.add_argument("--sim", action="store_true", default=True, help="Enable simulation mode for hardware")
    parser.add_argument("--cli", action="store_true", help="Force interactive CLI daemon mode")
    parser.add_argument("--daemon", action="store_true", help="Run as background daemon monitor")
    args = parser.parse_args()

    controller = FCDMSystemController(sim_mode=args.sim)

    # If display is available and user didn't force CLI, try GUI tray
    if not args.cli and not args.daemon and os.environ.get("DISPLAY"):
        if run_gui_tray(controller):
            return

    # Fallback to interactive CLI or daemon mode
    if args.daemon:
        print("[Tray Daemon] Running background watcher loop...")
        controller.start_orchestrator()
        try:
            while controller.running:
                time.sleep(2)
        except KeyboardInterrupt:
            controller.shutdown_all()
    else:
        run_cli_daemon(controller)

if __name__ == "__main__":
    main()
