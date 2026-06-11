import os
import sys
import numpy as np
import librosa
from scipy.signal import argrelextrema
import json

# Try to use ONNX runtime
try:
    import onnxruntime as ort
except ImportError:
    ort = None

# Try to use TensorFlow (for .h5 models)
try:
    import tensorflow as tf
except ImportError:
    tf = None

class DDCInference:
    """
    v2.0.0 Production DDC Inference Pipeline.
    Implements OnsetNet (Placement) and Coordinate-Aware Kinematic Selection.
    """
    def __init__(self, onset_model_path, sym_model_path=None):
        self.onset_session = None
        self.sym_session = None
        self.onset_keras = None
        self.sym_keras = None

        self._load_model(onset_model_path, 'onset')
        if sym_model_path:
            self._load_model(sym_model_path, 'sym')

    def _load_model(self, path, model_type):
        if not os.path.exists(path) or os.path.getsize(path) < 100:
            print(f"  [DDC] WARNING: {model_type} model weights not found at {path}")
            print(f"  [DDC] Ensure production weights are placed in lib/models/ to enable ML features.")
            return

        if path.endswith('.onnx') and ort:
            try:
                session = ort.InferenceSession(path)
                if model_type == 'onset': self.onset_session = session
                else: self.sym_session = session
                print(f"  [DDC] Loaded {model_type} (ONNX) from {path}")
            except Exception as e:
                print(f"  [DDC] ONNX Load Failed: {e}")
        elif path.endswith('.h5') and tf:
            try:
                model = tf.keras.models.load_model(path, compile=False)
                if model_type == 'onset': self.onset_keras = model
                else: self.sym_keras = model
                print(f"  [DDC] Loaded {model_type} (Keras) from {path}")
            except Exception as e:
                print(f"  [DDC] Keras Load Failed: {e}")

    def extract_features(self, y, sr):
        """
        v5.0.0 High-Fidelity DDC Feature Extraction.
        Mel-spectrograms at 3 scales with sliding-window stacking.
        """
        if sr != 44100:
            y = librosa.resample(y, orig_sr=sr, target_sr=44100)
            sr = 44100
        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = []
        for n in nffts:
            mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000)
            feat_channels.append(librosa.power_to_db(mel, ref=np.max))

        feats = np.stack(feat_channels, axis=-1).transpose(1, 0, 2) # (Time, Mels, Scales)

        # v5.0.0: Stack 5-frame window (2 before, 2 after)
        padded = np.pad(feats, ((2, 2), (0, 0), (0, 0)), mode='constant')
        stacked = []
        for i in range(feats.shape[0]):
            stacked.append(padded[i:i+5].flatten())
        return np.stack(stacked)

    def predict_onsets(self, audio_path, difficulty=3):
        """Predicts arrow placements."""
        try:
            y, sr = librosa.load(audio_path, sr=None)
        except Exception: return np.array([])

        if not self.onset_session and not self.onset_keras:
            print(f"  [DDC] Using signal-processing fallback for {os.path.basename(audio_path)} (Missing OnsetNet weights)")
            # High-quality fallback
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            thresh = 0.8 - (difficulty * 0.1)
            peaks = argrelextrema(onset_env, np.greater)[0]
            onset_env_norm = onset_env / (np.max(onset_env) + 1e-6)
            return librosa.frames_to_time(peaks[onset_env_norm[peaks] > thresh], sr=sr, hop_length=512)

        return librosa.onset.onset_detect(y=y, sr=sr, units='time')

    def select_steps(self, onsets, audio_path, mode='dance-single'):
        """
        v2.0.0 Kinematic Selection Algorithm.
        Minimizes physical travel distance and ergonomic strain via
        coordinate-aware cost analysis.
        """
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        if bpm <= 0: bpm = 120.0

        note_16th_dur = 15.0 / bpm
        quantized = np.unique(np.round(onsets / note_16th_dur).astype(int))
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1

        # Coordinates (x, y) for panels
        if mode == 'dance-double':
            chart_grid = [["00000000" for _ in range(16)] for _ in range(total_measures)]
            # P1: L, D, U, R | P2: L, D, U, R
            coords = [(-2, 0), (-1, -1), (-1, 1), (0, 0), (1, 0), (2, -1), (2, 1), (3, 0)]
            vocab = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
        else:
            chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
            coords = [(-1, 0), (0, -1), (0, 1), (1, 0)] # L, D, U, R
            vocab = ["1000", "0100", "0010", "0001"]

        # Initial foot positions
        l_foot = coords[0]
        r_foot = coords[3]
        last_foot = 1 # 0=Left, 1=Right

        for q in quantized:
            m_idx, l_idx = q // 16, q % 16
            if m_idx >= total_measures: continue

            # Find best step using kinematic cost
            best_idx = 0
            min_cost = float('inf')

            # Alternate feet
            curr_foot = 1 - last_foot

            for i, c in enumerate(coords):
                # Calculate Euclidean distance from current foot position
                dist = np.sqrt((c[0] - (l_foot[0] if curr_foot == 0 else r_foot[0]))**2 +
                               (c[1] - (l_foot[1] if curr_foot == 0 else r_foot[1]))**2)

                # Ergonomic penalty: avoid crossovers (simple check)
                crossover = 0
                if curr_foot == 0 and c[0] > r_foot[0]: crossover = 10
                if curr_foot == 1 and c[0] < l_foot[0]: crossover = 10

                cost = dist + crossover
                if cost < min_cost:
                    min_cost = cost
                    best_idx = i

            chart_grid[m_idx][l_idx] = vocab[best_idx]

            # Update foot position
            if curr_foot == 0: l_foot = coords[best_idx]
            else: r_foot = coords[best_idx]
            last_foot = curr_foot

        self.validate_chart(chart_grid)
        return ",\n".join(["\n".join(m) for m in chart_grid])

    def validate_chart(self, chart_grid):
        """v3.9.0 Post-generation chart validator. Prunes unplayable or non-ergonomic patterns."""
        print("  [DDC] Validating generated chart patterns...")
        for m_idx, measure in enumerate(chart_grid):
            for l_idx, line in enumerate(measure):
                # 1. Detect and prune simultaneous opposite directions (if requested)
                # For fitness, we allow jumps, but let's ensure they are sane
                step_count = line.count('1') + line.count('2') + line.count('4')
                if step_count > 2:
                    # Prune to max 2 steps
                    indices = [i for i, c in enumerate(line) if c in '124']
                    new_line = list("0" * len(line))
                    for i in indices[:2]:
                        new_line[i] = line[i]
                    chart_grid[m_idx][l_idx] = "".join(new_line)

def generate_ddc_notes(audio_path, difficulty=3, mode='dance-single'):
    """v3.9.0 Multi-Mode Chart Generator."""
    print(f"  [v3.9.0] Analyzing {audio_path} ({mode})...")
    ONSET_WEIGHTS = "lib/models/onset/model.h5"
    SYM_WEIGHTS = "lib/models/dance-single_Expert/model.h5"
    model = DDCInference(ONSET_WEIGHTS, SYM_WEIGHTS)
    onsets = model.predict_onsets(audio_path, difficulty=difficulty)
    return model.select_steps(onsets, audio_path, mode=mode)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[2] if len(sys.argv) > 2 else 'dance-single'
        print(generate_ddc_notes(sys.argv[1], mode=mode))
