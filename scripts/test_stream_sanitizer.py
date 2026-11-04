import unittest
import os
import subprocess
import tempfile

class TestStreamSanitizer(unittest.TestCase):
    """
    Validates stream sanitization behavior via the Go Orchestrator native sanitizer.
    """
    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.orchestrator = os.path.join(cls.repo_root, "fcdm-orchestrator")
        if not os.path.exists(cls.orchestrator):
            cls.orchestrator = os.path.join(cls.repo_root, "src/go-orchestrator/go-orchestrator")

    def _run_sanitizer(self, ssc_text):
        with tempfile.NamedTemporaryFile("w+", suffix=".ssc", delete=False) as infile:
            infile.write(ssc_text)
            in_name = infile.name

        out_name = in_name + ".sanitized.ssc"
        try:
            res = subprocess.run(
                [self.orchestrator, "--sanitize", in_name, "--out", out_name],
                capture_output=True,
                check=True
            )
            with open(out_name, "r") as f:
                return f.read()
        finally:
            if os.path.exists(in_name):
                os.remove(in_name)
            if os.path.exists(out_name):
                os.remove(out_name)

    def test_no_hands(self):
        chart = "//---------------\n#NOTES:\n1111\n0000\n;"
        sanitized = self._run_sanitizer(chart)
        self.assertIn("1100", sanitized)
        self.assertNotIn("1111", sanitized)

    def test_no_jacks(self):
        # 1000 followed by 1000 should see the second one removed
        chart = "//---------------\n#NOTES:\n1000\n1000\n;"
        sanitized = self._run_sanitizer(chart).replace(';', '')
        lines = [l.strip() for l in sanitized.split('\n') if l.strip() and not l.startswith("//") and not l.startswith("#")]
        self.assertEqual(lines[0], "1000")
        self.assertEqual(lines[1], "0000")

    def test_alternating_flow(self):
        chart = "//---------------\n#NOTES:\n1000\n0100\n0100\n0010\n;"
        sanitized = self._run_sanitizer(chart).replace(';', '')
        lines = [l.strip() for l in sanitized.split('\n') if l.strip() and not l.startswith("//") and not l.startswith("#")]
        self.assertEqual(lines[0], "1000")
        self.assertEqual(lines[1], "0100")
        self.assertEqual(lines[2], "0000") # Jack removed
        self.assertEqual(lines[3], "0010")

if __name__ == '__main__':
    unittest.main()
