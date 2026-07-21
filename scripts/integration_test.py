import os
import sys
import unittest
import subprocess

# Ensure we can import from the scripts directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stream_sanitizer import process_chart

class StagingIntegrationTest(unittest.TestCase):
    def test_pipeline_components(self):
        """Verify that core pipeline logic is intact for staging."""
        # 1. Test Stream Sanitizer (Core Logic)
        test_chart = """#NOTES:
0000
1001
1111
;"""
        sanitized = process_chart(test_chart)
        # Verify '1111' (4 notes) was reduced to max 2 notes
        self.assertIn("1100", sanitized)
        self.assertNotIn("1111", sanitized)
        print("Integration: Stream Sanitizer check passed.")

    def test_theme_integrity(self):
        """Verify that critical theme files exist in the expected structure."""
        theme_path = "themes/FitnessKiosk"
        required_files = [
            "metrics.ini",
            "Scripts/FitnessDifficulties.lua",
            "Scripts/00_init.lua",
            "BGAnimations/ScreenWorkoutSummary overlay/default.lua",
            "BGAnimations/ScreenFeedback overlay/default.lua",
            "Graphics/MusicWheelItem Song NormalPart/default.lua",
        ]
        for f in required_files:
            full_path = os.path.join(theme_path, f)
            self.assertTrue(os.path.exists(full_path), f"Missing critical theme file: {full_path}")
        print("Integration: Theme integrity check passed.")

    def test_kiosk_scripts(self):
        """Verify that kiosk deployment scripts exist and are executable."""
        scripts = ["scripts/fcdm_launch_production.sh", "scripts/dance-machine.service", "run_pipeline.py"]
        for s in scripts:
            self.assertTrue(os.path.exists(s), f"Missing deployment script: {s}")
        self.assertTrue(os.access("scripts/fcdm_launch_production.sh", os.X_OK), "fcdm_launch_production.sh is not executable")
        print("Integration: Kiosk scripts check passed.")

    def test_go_orchestrator_build(self):
        """Verify the new Go Orchestrator compiles and runs in sim-validate mode."""
        build = subprocess.run(["go", "build"], cwd="src/go-orchestrator", capture_output=True)
        self.assertEqual(build.returncode, 0, f"Go Orchestrator failed to compile: {build.stderr.decode('utf-8')}")

        run = subprocess.run(["./go-orchestrator", "--sim", "--validate"], cwd="src/go-orchestrator", capture_output=True)
        self.assertEqual(run.returncode, 0, f"Go Orchestrator failed validation: {run.stderr.decode('utf-8')}")
        self.assertIn("Pipeline integrity verified", run.stdout.decode('utf-8'))
        print("Integration: Go Orchestrator binary compiled and validated.")

if __name__ == "__main__":
    unittest.main()
