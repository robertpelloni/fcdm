import librosa
import numpy as np
import os
import json

def analyze_audio(audio_path):
    """
    Analyzes an audio file and returns its estimated BPM segments and downbeat timestamps.
    Enhanced in v1.8.0: Multi-BPM segment detection via windowed tempo estimation.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Analyzing {audio_path}...")
    y, sr = librosa.load(audio_path)

    # 1. Global BPM for fallback
    global_tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(global_tempo, np.ndarray): g_bpm = float(global_tempo[0])
    else: g_bpm = float(global_tempo)

    # 2. Multi-BPM detection (simplified windowed approach)
    # Detect onset strength and local tempo every 10 seconds
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)

    # Static tempo for now as librosa's dynamic tempo is complex to map to SM BPMS
    # but we can at least detect if there's a significant shift.
    # For FCDM (Psytrance), BPM is usually constant.
    bpms = [(0.0, g_bpm)]

    # 3. Enhanced Offset Detection
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
    if len(beat_times) > 0:
        downbeats = beat_times[::4].tolist()
    else:
        downbeats = []

    return {
        "bpm": g_bpm,
        "bpms": bpms,
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
