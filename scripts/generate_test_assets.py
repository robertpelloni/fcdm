import wave
import struct
import numpy as np
import os

def create_dummy_wav(path, duration=2.0, bpm=120):
    sr = 22050
    t = np.linspace(0, duration, int(sr * duration))
    y = np.sin(2 * np.pi * 440 * t)
    # Add clicks at BPM
    interval = 60.0 / bpm
    for i in range(int(duration / interval)):
        start = int(i * interval * sr)
        end = start + int(0.1 * sr)
        if end < len(y):
            y[start:end] = np.sin(2 * np.pi * 880 * t[start:end])

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((y * 32767).astype(np.int16).tobytes())
    print(f"Created {path}")

if __name__ == "__main__":
    create_dummy_wav("tests/assets/test_120bpm.wav", duration=5.0, bpm=120)
