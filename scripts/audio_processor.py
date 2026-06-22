import librosa
import numpy as np
import os
import json
from scipy.signal import argrelextrema

def analyze_audio(audio_path):
    """
    v13.0.0 Industrial-Diamond Multi-BPM Analysis.
    Windowed tempo estimation and sub-beat alignment for complex psytrance tracks.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Analyzing {audio_path}...")
    y, sr = librosa.load(audio_path, sr=44100)
    duration = librosa.get_duration(y=y, sr=sr)

    # 1. Global BPM Track
    global_tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    g_bpm = float(global_tempo[0]) if isinstance(global_tempo, (np.ndarray, list)) else float(global_tempo)

    # 2. Multi-BPM Segment Detection
    # Scan in 30s windows to detect significant tempo shifts
    bpms = []
    window_sec = 30
    for start_t in range(0, int(duration), window_sec):
        end_t = min(start_t + window_sec, duration)
        y_seg = y[int(start_t*sr):int(end_t*sr)]

        # We need at least 10 seconds for a reliable windowed beat track
        if len(y_seg) < sr * 10:
            continue

        t_seg, _ = librosa.beat.beat_track(y=y_seg, sr=sr)
        b_seg = float(t_seg[0]) if isinstance(t_seg, (np.ndarray, list)) else float(t_seg)

        # Only record if it differs significantly (>0.5 BPM) from the previous segment
        if not bpms or abs(bpms[-1][1] - b_seg) > 0.5:
            # Check for common harmonics (double/half time) and normalize to global neighborhood
            if abs(b_seg*2 - g_bpm) < 2.0: b_seg *= 2
            if abs(b_seg/2 - g_bpm) < 2.0: b_seg /= 2

            bpms.append((float(start_t), round(b_seg, 3)))

    if not bpms:
        bpms = [(0.0, round(g_bpm, 3))]

    # 3. Sub-beat Offset Detection
    # Align offset with the first high-strength onset
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_times = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)

    # Identify local maxima in onset strength
    peaks = argrelextrema(onset_env, np.greater)[0]
    if len(peaks) > 0:
        # Use a dynamic threshold (50% of the maximum onset in the first 10 seconds)
        first_10s_idx = librosa.time_to_frames(10.0, sr=sr)
        local_max = np.max(onset_env[:first_10s_idx]) if first_10s_idx < len(onset_env) else np.max(onset_env)
        thresh = local_max * 0.5

        significant_peaks = peaks[onset_env[peaks] > thresh]
        if len(significant_peaks) > 0:
            offset = onset_times[significant_peaks[0]]
        else:
            offset = onset_times[peaks[0]]
    else:
        offset = librosa.frames_to_time(beats[0], sr=sr) if len(beats) > 0 else 0.0

    beat_times = librosa.frames_to_time(beats, sr=sr)
    downbeats = beat_times[::4].tolist()

    return {
        "bpm": round(g_bpm, 3),
        "bpms": bpms,
        "offset": round(offset, 3),
        "downbeats": downbeats,
        "sample_rate": sr,
        "duration": round(duration, 3)
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 audio_processor.py <path_to_audio>")
        sys.exit(1)
    try:
        results = analyze_audio(sys.argv[1])
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
