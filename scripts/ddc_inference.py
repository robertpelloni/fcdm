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
    v3.0.0 Production DDC Inference Pipeline.
    Supports OnsetNet and Native SymNet via ONNX (.onnx) or Keras (.h5).
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
        if not os.path.exists(path): return

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
        """DDC Feature Extraction: Mel-spectrograms at 3 scales."""
        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = []
        for n in nffts:
            mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000)
            feat_channels.append(librosa.power_to_db(mel, ref=np.max))
        return np.stack(feat_channels, axis=-1).transpose(1, 0, 2)

    def predict_onsets(self, audio_path, difficulty=3):
        """Predicts arrow placements."""
        try:
            y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return np.array([])

        if not self.onset_session and not self.onset_keras:
            # High-quality fallback
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            thresh = 0.8 - (difficulty * 0.1)
            peaks = argrelextrema(onset_env, np.greater)[0]
            onset_env_norm = onset_env / (np.max(onset_env) + 1e-6)
            return librosa.frames_to_time(peaks[onset_env_norm[peaks] > thresh], sr=sr, hop_length=512)

        song_feats = self.extract_features(y, sr)
        n_frames = song_feats.shape[0]
        padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')
        feats_other = np.zeros((1, 5), dtype=np.float32)
        feats_other[0, max(0, min(4, difficulty-1))] = 1.0

        preds = []
        batch_size = 256
        for start in range(0, n_frames, batch_size):
            end = min(start + batch_size, n_frames)
            X_batch = np.array([padded[i:i+15] for i in range(start, end)]).astype(np.float32).reshape(-1, 1, 15, 80, 3)

            if self.onset_session:
                out = self.onset_session.run(None, {'audio_input:0': X_batch, 'other_input:0': np.repeat(feats_other, len(X_batch), axis=0)})[0]
                preds.extend(out.flatten())
            elif self.onset_keras:
                out = self.onset_keras.predict([X_batch, np.repeat(feats_other, len(X_batch), axis=0)], verbose=0)
                preds.extend(out.flatten())

        preds = np.array(preds)
        peaks = argrelextrema(preds, np.greater)[0]
        return librosa.frames_to_time(peaks[preds[peaks] > 0.5], sr=sr, hop_length=512)

    def select_steps(self, onsets, audio_path):
        """Predicts arrow directions using native recursive LSTM."""
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        if bpm <= 0: bpm = 120.0

        note_16th_dur = 15.0 / bpm
        quantized = np.unique(np.round(onsets / note_16th_dur).astype(int))
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1

        chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
        vocab = ["1000", "0100", "0010", "0001", "1100", "0011", "1010", "0101"]

        # --- Native LSTM Sequence Generation (v3.0.0) ---
        h = np.zeros((1, 256), dtype=np.float32)
        c = np.zeros((1, 256), dtype=np.float32)
        prev_idx = 0
        audio_feats = self.extract_features(y, sr)

        for q in quantized:
            m_idx, l_idx = q // 16, q % 16
            if m_idx >= total_measures: continue

            if self.sym_session or self.sym_keras:
                frame_idx = int(q * note_16th_dur / (512/sr))
                if frame_idx < audio_feats.shape[0]:
                    feat_audio = audio_feats[frame_idx].reshape(1, 1, -1).astype(np.float32)
                    feat_prev = np.zeros((1, 1, len(vocab)), dtype=np.float32)
                    feat_prev[0, 0, prev_idx] = 1.0
                    sym_input = np.concatenate([feat_audio, feat_prev], axis=-1)

                    try:
                        # Full recursive step
                        if self.sym_session:
                            out = self.sym_session.run(None, {'input': sym_input, 'h_in': h, 'c_in': c})
                            logits, h, c = out[0], out[1], out[2]
                        else:
                            out = self.sym_keras.predict([sym_input, h, c], verbose=0)
                            logits, h, c = out[0], out[1], out[2]

                        # Temperature-based sampling for pattern variety
                        probs = np.exp(logits[0, 0]) / np.sum(np.exp(logits[0, 0]))
                        prev_idx = np.random.choice(len(vocab), p=probs)
                    except Exception:
                        prev_idx = q % len(vocab)
            else:
                prev_idx = q % 4

            chart_grid[m_idx][l_idx] = vocab[prev_idx]

        return ",\n".join(["\n".join(m) for m in chart_grid])

def generate_ddc_notes(audio_path, difficulty=3):
    """v3.0.0 High-Fidelity Chart Generator."""
    print(f"  [v3.0.0] Processing {audio_path}...")
    ONSET_WEIGHTS = "lib/models/onset/model.h5"
    SYM_WEIGHTS = "lib/models/dance-single_Expert/model.h5"
    model = DDCInference(ONSET_WEIGHTS, SYM_WEIGHTS)
    onsets = model.predict_onsets(audio_path, difficulty=difficulty)
    return model.select_steps(onsets, audio_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_ddc_notes(sys.argv[1]))
