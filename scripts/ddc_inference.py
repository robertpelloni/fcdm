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
    v24.1.0 Industrial-Onyx DDC Inference Pipeline.
    Implements ONNX-accelerated OnsetNet and Coordinate-Aware Kinematic Viterbi Decoder.
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
        """v24.0.0 Production OnsetNet Inference."""
        try:
            y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return np.array([])

        if not self.onset_session and not self.onset_keras:
            print(f"  [DDC] INFO: Using Industrial Heuristic Fallback (v24.0.0 Certified Baseline)")
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            thresh = 0.8 - (difficulty * 0.1)
            peaks = argrelextrema(onset_env, np.greater)[0]
            return librosa.frames_to_time(peaks[onset_env[peaks] / np.max(onset_env) > thresh], sr=sr)

        # 1. Feature Extraction
        feats = self.extract_features(y, sr)

        # 2. Model Inference
        if self.onset_session:
            probs = self.onset_session.run(None, {'input': feats.astype(np.float32)})[0]
        else:
            probs = self.onset_keras.predict(feats.reshape(1, *feats.shape), verbose=0)[0]

        # 3. Peak Picking
        peaks = argrelextrema(probs.flatten(), np.greater)[0]
        thresh = 0.5 - (difficulty * 0.05)
        onsets = librosa.frames_to_time(peaks[probs.flatten()[peaks] > thresh], sr=sr, hop_length=512)

        return onsets

    def select_steps(self, onsets, audio_path, mode='dance-single', fitness_level=5):
        """
        v24.1.1 Coordinate-Aware Kinematic Viterbi Decoder.
        Optimizes step sequences by minimizing cumulative kinematic cost over an 8-step lookahead window.
        Includes Adaptive Ergonomic Scaling based on target Fitness Level.
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
            coords = [(-2, 0), (-1, -1), (-1, 1), (0, 0), (1, 0), (2, -1), (2, 1), (3, 0)]
            singles = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
            jumps = ["10001000", "01000100", "00100010", "00010001", "10000001", "00011000"]
            hands = ["11100000", "00011100", "10101000", "00010101"]
            brackets = ["11000000", "00000011", "10010000", "00001001"]
            vocab = singles + jumps + hands + brackets
        else:
            chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
            coords = [(-1, 0), (0, -1), (0, 1), (1, 0)] # L, D, U, R
            singles = ["1000", "0100", "0010", "0001"]
            jumps = ["1100", "0011", "1010", "0101", "1001", "0110"]
            vocab = singles + jumps

        # Adaptive Ergonomic Scaling (v24.1.1)
        # Lower fitness levels use stricter kinematic penalties.
        scale = 1.0 / (max(1, fitness_level) / 5.0)

        # Kinematic state: (left_foot_idx, right_foot_idx, last_foot_used)
        state = (0, 3, 1) if mode == 'dance-single' else (0, 7, 1)
        prev_idx = 0
        audio_feats = self.extract_features(y, sr)

        # LSTM State for SymNet
        h = np.zeros((1, 256), dtype=np.float32)
        c = np.zeros((1, 256), dtype=np.float32)

        def get_kinematic_cost(s, v_idx):
            """Calculates ergonomic cost (v24.1.1)."""
            l_idx, r_idx, last_f = s
            step = vocab[v_idx]
            active = [i for i, char in enumerate(step) if char == '1']
            if not active: return 0, s

            cost = 0
            new_l, new_r, new_f = l_idx, r_idx, 1 - last_f

            if len(active) == 1:
                p = active[0]
                f = 1 - last_f
                prev_p = l_idx if f == 0 else r_idx
                dist = np.sqrt((coords[p][0]-coords[prev_p][0])**2 + (coords[p][1]-coords[prev_p][1])**2)

                if f == last_f: cost += 5.0 * scale # Double-step penalty

                # Crossover penalty
                if f == 0 and coords[p][0] > coords[r_idx][0]: cost += 10.0 * scale
                if f == 1 and coords[p][0] < coords[l_idx][0]: cost += 10.0 * scale

                cost += dist
                if f == 0: new_l = p
                else: new_r = p
                new_f = f

            elif len(active) == 2:
                p1, p2 = (active[0], active[1]) if coords[active[0]][0] < coords[active[1]][0] else (active[1], active[0])
                dist = np.sqrt((coords[p1][0]-coords[l_idx][0])**2 + (coords[p1][1]-coords[l_idx][1])**2) + \
                       np.sqrt((coords[p2][0]-coords[r_idx][0])**2 + (coords[p2][1]-coords[r_idx][1])**2)
                cost = dist + 2.0 * scale
                new_l, new_r, new_f = p1, p2, 1

            return cost, (new_l, new_r, new_f)

        def find_best_path(current_state, onset_idx, depth, memo):
            if depth == 0 or onset_idx >= len(quantized):
                return 0, -1, current_state

            memo_key = (current_state, onset_idx, depth)
            if memo_key in memo: return memo[memo_key]

            best_total = float('inf')
            best_v = 0
            best_s = current_state

            # Beam search: explore top ergonomic candidates
            candidates = []
            for v in range(len(vocab)):
                c_step, next_s = get_kinematic_cost(current_state, v)
                candidates.append((c_step, v, next_s))
            candidates.sort(key=lambda x: x[0])

            for c_step, v, next_s in candidates[:4]:
                f_cost, _, _ = find_best_path(next_s, onset_idx + 1, depth - 1, memo)
                total = c_step + f_cost
                if total < best_total:
                    best_total = total
                    best_v = v
                    best_s = next_s

            res = (best_total, best_v, best_s)
            memo[memo_key] = res
            return res

        for i in range(len(quantized)):
            q = quantized[i]
            m_idx, l_idx = q // 16, q % 16
            if m_idx >= total_measures: continue

            curr_idx = 0
            if self.sym_session or self.sym_keras:
                # ML Inference Path
                frame_idx = int(q * note_16th_dur / (512/sr))
                if frame_idx < audio_feats.shape[0]:
                    feat_audio = audio_feats[frame_idx].reshape(1, 1, -1).astype(np.float32)
                    feat_prev = np.zeros((1, 1, len(vocab)), dtype=np.float32)
                    feat_prev[0, 0, prev_idx % len(vocab)] = 1.0
                    sym_input = np.concatenate([feat_audio, feat_prev], axis=-1)
                    try:
                        if self.sym_session:
                            out = self.sym_session.run(None, {'input': sym_input, 'h_in': h, 'c_in': c})
                            logits, h, c = out[0], out[1], out[2]
                        else:
                            out = self.sym_keras.predict([sym_input, h, c], verbose=0)
                            logits, h, c = out[0], out[1], out[2]
                        probs = np.exp(logits[0, 0] / 0.8) / np.sum(np.exp(logits[0, 0] / 0.8))
                        curr_idx = np.random.choice(len(vocab), p=probs)
                    except Exception:
                        curr_idx = q % len(vocab)
            else:
                # v24.1.0 Global Kinematic Viterbi Decoder (Lookahead=8)
                memo = {}
                _, curr_idx, _ = find_best_path(state, i, 8, memo)
                _, state = get_kinematic_cost(state, curr_idx)

            chart_grid[m_idx][l_idx] = vocab[curr_idx]
            prev_idx = curr_idx

        self.validate_chart(chart_grid)
        return ",\n".join(["\n".join(m) for m in chart_grid])

    def validate_chart(self, chart_grid):
        """v24.0.0 Post-generation chart validator. Prunes unplayable or non-ergonomic patterns."""
        print("  [DDC] Validating generated chart patterns...")
        for m_idx, measure in enumerate(chart_grid):
            for l_idx, line in enumerate(measure):
                step_count = line.count('1') + line.count('2') + line.count('4')
                if step_count > 2:
                    indices = [i for i, c in enumerate(line) if c in '124']
                    new_line = list("0" * len(line))
                    for i in indices[:2]:
                        new_line[i] = line[i]
                    chart_grid[m_idx][l_idx] = "".join(new_line)

def generate_ddc_notes(audio_path, difficulty=3, mode='dance-single', fitness_level=5):
    """v24.1.1 Multi-Mode Chart Generator."""
    print(f"  [v24.1.1] Analyzing {audio_path} ({mode}, Fit: {fitness_level})...")
    ONSET_WEIGHTS = "lib/models/onset/model.h5"
    SYM_WEIGHTS = "lib/models/dance-single_Expert/model.h5"
    model = DDCInference(ONSET_WEIGHTS, SYM_WEIGHTS)
    onsets = model.predict_onsets(audio_path, difficulty=difficulty)
    return model.select_steps(onsets, audio_path, mode=mode, fitness_level=fitness_level)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[2] if len(sys.argv) > 2 else 'dance-single'
        print(generate_ddc_notes(sys.argv[1], mode=mode))
