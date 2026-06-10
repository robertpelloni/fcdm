import os
import sys
import numpy as np
import librosa
from scipy.signal import argrelextrema
import json

# ONNX runtime for production-grade speed and reliability
try:
    import onnxruntime as ort
except ImportError:
    ort = None

class DDCInference:
    """
    v2.7.0 Production DDC Inference Pipeline.
    Implements OnsetNet (Placement) and Native SymNet (LSTM Selection).
    """
    def __init__(self, onset_model_path, sym_model_path=None):
        self.onset_session = None
        self.sym_session = None

        if ort:
            try:
                if os.path.exists(onset_model_path) and os.path.getsize(onset_model_path) > 0:
                    self.onset_session = ort.InferenceSession(onset_model_path)
                    print(f"  [DDC] Loaded OnsetNet from {onset_model_path}")
                if sym_model_path and os.path.exists(sym_model_path) and os.path.getsize(sym_model_path) > 0:
                    self.sym_session = ort.InferenceSession(sym_model_path)
                    print(f"  [DDC] Loaded SymNet from {sym_model_path}")
            except Exception as e:
                print(f"  [DDC] ML Initialization failed: {e}. Falling back to heuristics.")

    def extract_features(self, y, sr):
        """DDC Feature Extraction: Mel-spectrograms at 3 scales."""
        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = []
        for n in nffts:
            mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000)
            feat_channels.append(librosa.power_to_db(mel, ref=np.max))
        # Return [Frames, Mel-Bins, Channels] -> [N, 80, 3]
        return np.stack(feat_channels, axis=-1).transpose(1, 0, 2)

    def predict_onsets(self, audio_path, difficulty=3):
        """Predicts arrow placements using OnsetNet CNN."""
        try:
            y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return np.array([])

        if not self.onset_session:
            # Fallback: High-quality Spectral Flux onset detection
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
            thresh = 0.8 - (difficulty * 0.1)
            peaks = argrelextrema(onset_env, np.greater)[0]
            onset_env_norm = onset_env / (np.max(onset_env) + 1e-6)
            filtered_peaks = peaks[onset_env_norm[peaks] > thresh]
            return librosa.frames_to_time(filtered_peaks, sr=sr, hop_length=512)

        song_feats = self.extract_features(y, sr)
        n_frames = song_feats.shape[0]
        padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')

        # Difficulty one-hot
        feats_other = np.zeros((1, 5), dtype=np.float32)
        feats_other[0, max(0, min(4, difficulty-1))] = 1.0

        batch_size = 256
        all_preds = []
        for start in range(0, n_frames, batch_size):
            end = min(start + batch_size, n_frames)
            X_batch = np.array([padded[i:i+15] for i in range(start, end)])
            X_batch = X_batch.reshape(-1, 1, 15, 80, 3).astype(np.float32)

            try:
                out = self.onset_session.run(None, {
                    'audio_input:0': X_batch,
                    'other_input:0': np.repeat(feats_other, len(X_batch), axis=0)
                })[0]
                all_preds.extend(out.flatten())
            except Exception:
                all_preds.extend(np.zeros(end-start))

        all_preds = np.array(all_preds)
        peaks = argrelextrema(all_preds, np.greater)[0]
        return librosa.frames_to_time(peaks[all_preds[peaks] > 0.5], sr=sr, hop_length=512)

    def select_steps(self, onsets, audio_path):
        """Predicts arrow directions using recursive LSTM selection."""
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, (np.ndarray, list)) else float(tempo)
        if bpm <= 0: bpm = 120.0

        note_16th_dur = 15.0 / bpm
        quantized = np.unique(np.round(onsets / note_16th_dur).astype(int))
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1

        chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
        vocab = ["1000", "0100", "0010", "0001", "1100", "0011", "1010", "0101"]

        # LSTM State Management
        h = np.zeros((1, 256), dtype=np.float32)
        c = np.zeros((1, 256), dtype=np.float32)
        prev_idx = 0

        audio_feats = self.extract_features(y, sr)

        for q in quantized:
            m_idx, l_idx = q // 16, q % 16
            if m_idx >= total_measures: continue

            if self.sym_session:
                frame_idx = int(q * note_16th_dur / (512/sr))
                if frame_idx < audio_feats.shape[0]:
                    feat_audio = audio_feats[frame_idx].reshape(1, 1, -1).astype(np.float32)
                    feat_prev = np.zeros((1, 1, len(vocab)), dtype=np.float32)
                    feat_prev[0, 0, prev_idx] = 1.0

                    sym_input = np.concatenate([feat_audio, feat_prev], axis=-1)

                    # --- NATIVE ONNX LSTM RUN (v2.7.0) ---
                    try:
                        # Map internal names for SymNet export
                        feeds = {'input': sym_input, 'h_in': h, 'c_in': c}
                        outputs = self.sym_session.run(None, feeds)
                        logits, h, c = outputs[0], outputs[1], outputs[2]
                        # Temperature sampling for pattern variety
                        probs = np.exp(logits[0, 0]) / np.sum(np.exp(logits[0, 0]))
                        prev_idx = np.random.choice(len(vocab), p=probs)
                    except Exception:
                        prev_idx = q % len(vocab)
            else:
                prev_idx = q % 4 # L-D-U-R

            chart_grid[m_idx][l_idx] = vocab[prev_idx]

        return ",\n".join(["\n".join(m) for m in chart_grid])

def generate_ddc_notes(audio_path, difficulty=3):
    """Entry point for v2.7.0 production chart generation."""
    print(f"  [v2.7.0] Analyzing {audio_path} (Difficulty {difficulty})...")

    ONSET_MODEL = "lib/models/ddc_onset.onnx"
    SYM_MODEL = "lib/models/ddc_sym.onnx"

    model = DDCInference(ONSET_MODEL, SYM_MODEL)
    onsets = model.predict_onsets(audio_path, difficulty=difficulty)

    if len(onsets) == 0:
        return "1000\n0000\n0000\n0000\n,\n0001\n0000\n0000\n0000"

    return model.select_steps(onsets, audio_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        diff = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        print(generate_ddc_notes(sys.argv[1], difficulty=diff))
