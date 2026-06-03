import unittest
import os
from stream_sanitizer import process_chart

class TestStreamSanitizer(unittest.TestCase):
    def test_no_hands(self):
        chart = "#NOTES:\n1111\n0000\n;"
        sanitized = process_chart(chart)
        self.assertIn("1100", sanitized)
        self.assertNotIn("1111", sanitized)

    def test_no_jacks(self):
        # 1000 followed by 1000 should see the second one removed
        chart = "#NOTES:\n1000\n1000\n;"
        sanitized = process_chart(chart).replace(';', '')
        lines = [l.strip() for l in sanitized.split('\n') if l.strip()]
        self.assertEqual(lines[1], "1000")
        self.assertEqual(lines[2], "0000")

    def test_alternating_flow(self):
        chart = "#NOTES:\n1000\n0100\n0100\n0010\n;"
        sanitized = process_chart(chart).replace(';', '')
        lines = [l.strip() for l in sanitized.split('\n') if l.strip()]
        self.assertEqual(lines[1], "1000")
        self.assertEqual(lines[2], "0100")
        self.assertEqual(lines[3], "0000") # Jack removed
        self.assertEqual(lines[4], "0010")

if __name__ == '__main__':
    unittest.main()
