import os
import sys
import librosa
import numpy as np

def analyze_audio(file_path):
    """
    Analyzes an audio file to extract BPM and beat onsets for rhythm game chart generation.
    Returns the BPM and a list of onset times in seconds.
    """
    print(f"  [AudioProcessor] Analyzing {file_path}...")

    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)

    # Extract tempo and beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Simple onset detection for finer rhythmic details (beyond just the main beat)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Filter onsets to only include those that align relatively well with the beat grid
    # or just use the raw beat times as the primary "steps" for a pure cardio flow.
    # For a fitness machine, the primary beat is usually the safest target.

    # Handle tempo which might be returned as an array in newer librosa versions
    bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

    print(f"  [AudioProcessor] Detected BPM: {bpm:.2f}, Beats: {len(beat_times)}")

    return bpm, beat_times.tolist()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_processor.py <audio_file>")
        sys.exit(1)

    bpm, beats = analyze_audio(sys.argv[1])
    print(f"BPM: {bpm}")
    print(f"First 5 beats: {beats[:5]}")
