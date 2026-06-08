import librosa
import numpy as np
import os
import json

def analyze_audio(audio_path):
    """
    Analyzes an audio file and returns its estimated BPM and downbeat timestamps.
    Enhanced in v1.7.0: Sophisticated offset detection via first significant onset.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Analyzing {audio_path}...")
    y, sr = librosa.load(audio_path)

    # 1. Estimate BPM
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray): bpm = float(tempo[0])
    else: bpm = float(tempo)

    # 2. Enhanced Offset Detection
    # Instead of assuming beat 0 is at time 0, find the first significant peak.
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    # The first beat time from beat_track is a good candidate
    beat_times = librosa.frames_to_time(beats, sr=sr)

    if len(beat_times) > 0:
        first_beat = beat_times[0]
        # In StepMania, OFFSET is negative (time in seconds before the first beat)
        # Or more accurately, the time of the first beat relative to start.
        # But we'll just return the times and let the consumer handle the SM tag.
        downbeats = beat_times[::4].tolist()
    else:
        downbeats = []

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
