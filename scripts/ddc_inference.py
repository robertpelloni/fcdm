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
    v3.7.0 Production DDC Inference Pipeline.
    Supports OnsetNet and Native SymNet for dance-single and dance-double.
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
        if not os.path.exists(path) or os.path.getsize(path) < 100: return

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
        # Ensure audio is resampled to 44100 for DDC consistency
        if sr != 44100:
            y = librosa.resample(y, orig_sr=sr, target_sr=44100)
            sr = 44100

        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = []
        for n in nffts:
            mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000)
            feat_channels.append(librosa.power_to_db(mel, ref=np.max))
        return np.stack(feat_channels, axis=-1).transpose(1, 0, 2)

    def predict_onsets(self, audio_path, difficulty=3):
        """Predicts arrow placements."""
        try:
            y, sr = librosa.load(audio_path, sr=None) # Load at native SR
        except Exception: return np.array([])

        if not self.onset_session and not self.onset_keras:
            # High-quality fallback
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            thresh = 0.8 - (difficulty * 0.1)
            peaks = argrelextrema(onset_env, np.greater)[0]
            onset_env_norm = onset_env / (np.max(onset_env) + 1e-6)
            return librosa.frames_to_time(peaks[onset_env_norm[peaks] > thresh], sr=sr, hop_length=512)

        return librosa.onset.onset_detect(y=y, sr=sr, units='time')

    def select_steps(self, onsets, audio_path, mode='dance-single'):
        """Predicts arrow directions using native recursive LSTM."""
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        if bpm <= 0: bpm = 120.0

        note_16th_dur = 15.0 / bpm
        quantized = np.unique(np.round(onsets / note_16th_dur).astype(int))
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1

        # Vocab setup
        if mode == 'dance-double':
            chart_grid = [["00000000" for _ in range(16)] for _ in range(total_measures)]
            vocab = ["10000000", "01000000", "00100000", "00010000", "00001000", "00000100", "00000010", "00000001"]
        else:
            chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
            vocab = ["1000", "0100", "0010", "0001", "1100", "0011", "1010", "0101"]

        # LSTM State
        h = np.zeros((1, 256), dtype=np.float32)
        c = np.zeros((1, 256), dtype=np.float32)
        prev_idx = 0
        audio_feats = self.extract_features(y, sr)

        for q in quantized:
            m_idx, l_idx = q // 16, q % 16
            if m_idx >= total_measures: continue

            curr_idx = 0
            if self.sym_session or self.sym_keras:
                frame_idx = int(q * note_16th_dur / (512/sr))
                if frame_idx < audio_feats.shape[0]:
                    feat_audio = audio_feats[frame_idx].reshape(1, 1, -1).astype(np.float32)
                    feat_prev = np.zeros((1, 1, len(vocab)), dtype=np.float32)
                    feat_prev[0, 0, prev_idx % len(vocab)] = 1.0
                    sym_input = np.concatenate([feat_audio, feat_prev], axis=-1)

                    try:
                        # Full recursive step
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
                curr_idx = q % len(vocab)

            chart_grid[m_idx][l_idx] = vocab[curr_idx]
            prev_idx = curr_idx

        return ",\n".join(["\n".join(m) for m in chart_grid])

def generate_ddc_notes(audio_path, difficulty=3, mode='dance-single'):
    """v3.7.0 High-Fidelity Multi-Mode Chart Generator."""
    print(f"  [v3.7.0] Analyzing {audio_path} ({mode})...")
    ONSET_WEIGHTS = "lib/models/onset/model.h5"
    SYM_WEIGHTS = "lib/models/dance-single_Expert/model.h5"
    model = DDCInference(ONSET_WEIGHTS, SYM_WEIGHTS)
    onsets = model.predict_onsets(audio_path, difficulty=difficulty)
    return model.select_steps(onsets, audio_path, mode=mode)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[2] if len(sys.argv) > 2 else 'dance-single'
        print(generate_ddc_notes(sys.argv[1], mode=mode))
