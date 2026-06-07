import unittest
import os
import numpy as np
import wave
import struct
from scripts.audio_processor import analyze_audio

class TestAudioProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a synthetic beep at 120 BPM
        cls.test_audio = "test_120bpm.wav"
        cls.sample_rate = 22050
        duration = 5.0  # seconds
        bpm = 120
        beat_interval = 60.0 / bpm

        # Simple click track: a short 440Hz tone every beat
        t = np.linspace(0, duration, int(cls.sample_rate * duration), endpoint=False)
        y = np.zeros_like(t)

        for i in range(int(duration / beat_interval)):
            start_idx = int(i * beat_interval * cls.sample_rate)
            end_idx = start_idx + int(0.1 * cls.sample_rate) # 100ms click
            if end_idx < len(y):
                y[start_idx:end_idx] = np.sin(2 * np.pi * 440 * t[start_idx:end_idx])

        # Write to WAV
        with wave.open(cls.test_audio, 'w') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(cls.sample_rate)
            for sample in y:
                f.writeframes(struct.pack('<h', int(sample * 32767)))

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_audio):
            os.remove(cls.test_audio)

    def test_bpm_detection(self):
        results = analyze_audio(self.test_audio)
        print(f"Detected BPM: {results['bpm']}")
        # Librosa might be slightly off on short synthetic samples, but should be close to 120
        self.assertGreater(results['bpm'], 110)
        self.assertLess(results['bpm'], 130)

    def test_downbeat_detection(self):
        results = analyze_audio(self.test_audio)
        self.assertTrue(len(results['downbeats']) > 0)
        self.assertLess(results['downbeats'][0], 1.0) # Downbeat should be near start

if __name__ == "__main__":
    unittest.main()
