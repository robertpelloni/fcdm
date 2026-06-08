import librosa
import numpy as np
import os

def generate_notes(audio_path, difficulty="Medium", meter=5):
    """
    Generates a production-grade (fitness-optimized) chart using librosa signal processing.
    Uses onset detection and a circular flow state machine to ensure cardio-friendly movement.
    """
    if not os.path.exists(audio_path):
        return "0000\n,\n0000\n"

    print(f"  [Dancing2Night] Analyzing {audio_path} for chart generation...")
    y, sr = librosa.load(audio_path, sr=22050)

    # 1. Detect Tempo and Onsets
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, np.ndarray):
        bpm = float(tempo[0])
    else:
        bpm = float(tempo)

    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')

    # 2. Map onsets to the chart grid (16th notes)
    # 16th note duration in seconds = (60 / BPM) / 4
    note_16th_dur = 15.0 / bpm

    # Quantize onsets to 16th notes
    quantized_onsets = np.round(onsets / note_16th_dur).astype(int)
    unique_onsets = np.unique(quantized_onsets)

    if len(unique_onsets) == 0:
        return "0000\n,\n0000\n"

    max_16th = unique_onsets[-1]
    # Total measures needed (4 beats per measure, 4 16ths per beat = 16 16ths per measure)
    total_measures = (max_16th // 16) + 1

    # Create a grid of measures
    # Each measure is a list of 16 lines (4 beats * 4 16ths)
    chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]

    # 3. Circular Flow State Machine (L -> D -> U -> R -> L ...)
    # This ensures no double-steps and optimal fitness flow.
    flow_cycle = ["1000", "0100", "0010", "0001"]
    flow_idx = 0

    for o in unique_onsets:
        m_idx = o // 16
        l_idx = o % 16
        if m_idx < total_measures:
            chart_grid[m_idx][l_idx] = flow_cycle[flow_idx]
            flow_idx = (flow_idx + 1) % len(flow_cycle)

    # 4. Format into SSC/SM Measures
    measures_str = []
    for m in chart_grid:
        measures_str.append("\n".join(m))

    return ",\n".join(measures_str)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(generate_notes(sys.argv[1]))
    else:
        print("Usage: python3 dancing2night.py <audio_file>")
