import librosa
import numpy as np
import os
import json

def analyze_audio(audio_path):
    """
    Analyzes an audio file and returns its estimated BPM and downbeat timestamps.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Analyzing {audio_path}...")
    y, sr = librosa.load(audio_path)

    # 1. Estimate BPM
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    # tempo is now an array-like or float depending on version
    if isinstance(tempo, np.ndarray):
        bpm = float(tempo[0])
    else:
        bpm = float(tempo)

    # 2. Estimate Downbeats (simple heuristic: first beat of every 4 beats)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    downbeats = beat_times[::4].tolist()

    return {
        "bpm": bpm,
        "downbeats": downbeats,
        "sample_rate": sr,
        "duration": librosa.get_duration(y=y, sr=sr)
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 audio_processor.py <audio_file>")
        sys.exit(1)

    try:
        results = analyze_audio(sys.argv[1])
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
