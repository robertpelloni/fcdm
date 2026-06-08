import os
import sys
import unittest
import shutil
from scripts.stream_sanitizer import process_chart

class StagingIntegrationTest(unittest.TestCase):
    def test_pipeline_components(self):
        test_chart = "#NOTES:\n0000\n1001\n1111\n;"
        sanitized = process_chart(test_chart)
        self.assertIn("1100", sanitized)
        print("Integration: Stream Sanitizer check passed.")

    def test_theme_integrity(self):
        theme_path = "themes/FitnessKiosk"
        required_files = ["metrics.ini", "Scripts/FitnessDifficulties.lua", "Scripts/00_init.lua"]
        for f in required_files:
            self.assertTrue(os.path.exists(os.path.join(theme_path, f)))
        print("Integration: Theme integrity check passed.")

    def test_kiosk_scripts(self):
        scripts = ["scripts/kiosk-standalone.sh", "scripts/dance-machine.service", "scripts/ingest_music.py"]
        for s in scripts:
            self.assertTrue(os.path.exists(s))
        self.assertTrue(os.access("scripts/kiosk-standalone.sh", os.X_OK))
        print("Integration: Kiosk scripts check passed.")

    def test_stress_ingestion(self):
        stress_dir = "itgmania/Songs/StressTest"
        os.makedirs(os.path.join(stress_dir, "Batch1"), exist_ok=True)
        # Create valid but tiny wav files using wave module
        import wave, struct
        for i in range(3):
            path = os.path.join(stress_dir, "Batch1", f"stress_{i}.wav")
            with wave.open(path, 'w') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(22050)
                f.writeframes(struct.pack('<h', 0) * 1000)

        print("Integration: Starting Stress Test...")
        from scripts.ingest_music import ingest_songs
        ingest_songs(stress_dir)
        shutil.rmtree(stress_dir)
        print("Integration: Stress Test passed.")

if __name__ == "__main__":
    unittest.main()
