import os
import sys
import numpy as np
import librosa
from scipy.signal import argrelextrema

# Try to use ONNX runtime for production-grade speed and reliability
try:
    import onnxruntime as ort
except ImportError:
    ort = None

# Fallback to TensorFlow for legacy support if needed
try:
    import tensorflow as tf
    tf.compat.v1.disable_eager_execution()
except ImportError:
    tf = None

class DDCInference:
    def __init__(self, sp_model_path):
        self.sp_model_path = sp_model_path
        if ort and sp_model_path.endswith('.onnx'):
            self.mode = 'onnx'
            self.session = ort.InferenceSession(sp_model_path)
        elif tf:
            self.mode = 'tf'
            self.sess = tf.compat.v1.Session()
            self._build_sp_model()
            self._restore()
        else:
            raise RuntimeError("No suitable ML backend (ONNX or TF) found.")

    def _build_sp_model(self):
        with tf.compat.v1.variable_scope('model_sp'):
            self.audio_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 15, 80, 3], name='feats_audio')
            self.other_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 5], name='feats_other')
            feats_audio = tf.reshape(self.audio_input, shape=[-1, 15, 80, 3])
            feats_other = tf.reshape(self.other_input, shape=[-1, 5])
            w0, b0 = tf.compat.v1.get_variable('cnn_0/filters', [7, 3, 3, 10]), tf.compat.v1.get_variable('cnn_0/biases', [10])
            conv0 = tf.nn.conv2d(feats_audio, w0, [1, 1, 1, 1], padding='VALID')
            relu0 = tf.nn.relu(tf.nn.bias_add(conv0, b0))
            pool0 = tf.nn.max_pool2d(relu0, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')
            w1, b1 = tf.compat.v1.get_variable('cnn_1/filters', [3, 3, 10, 20]), tf.compat.v1.get_variable('cnn_1/biases', [20])
            conv1 = tf.nn.conv2d(pool0, w1, [1, 1, 1, 1], padding='VALID')
            relu1 = tf.nn.relu(tf.nn.bias_add(conv1, b1))
            pool1 = tf.nn.max_pool2d(relu1, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')
            flat_cnn = tf.reshape(pool1, [-1, 1120])
            feats_all = tf.concat([flat_cnn, feats_other], axis=1)
            wd0, bd0 = tf.compat.v1.get_variable('dnn_0/W', [1125, 256]), tf.compat.v1.get_variable('dnn_0/b', [256])
            dnn0 = tf.nn.relu(tf.matmul(feats_all, wd0) + bd0)
            wd1, bd1 = tf.compat.v1.get_variable('dnn_1/W', [256, 128]), tf.compat.v1.get_variable('dnn_1/b', [128])
            dnn1 = tf.nn.relu(tf.matmul(dnn0, wd1) + bd1)
            wl, bl = tf.compat.v1.get_variable('logit/W', [128, 1]), tf.compat.v1.get_variable('logit/b', [1])
            self.logits = tf.matmul(dnn1, wl) + bl
            self.prediction = tf.nn.sigmoid(self.logits)

    def _restore(self):
        tf.compat.v1.train.Saver(tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope='model_sp')).restore(self.sess, self.sp_model_path)

    def predict_onsets(self, audio_path, difficulty=3):
        try: y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return np.array([])
        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = [librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000), ref=np.max) for n in nffts]
        song_feats = np.stack(feat_channels, axis=-1).transpose(1, 0, 2)
        n_frames = song_feats.shape[0]
        padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')
        feats_other = np.zeros((1, 5), dtype=np.float32)
        feats_other[0, max(0, min(4, difficulty-1))] = 1.0

        batch_size, preds = 512, []
        for start in range(0, n_frames, batch_size):
            end = min(start + batch_size, n_frames)
            X_batch = np.array([padded[i:i+15] for i in range(start, end)])
            if self.mode == 'onnx':
                batch_preds = self.session.run(['model_sp/output_node:0'], {'audio_input:0': X_batch, 'other_input:0': np.repeat(feats_other, len(X_batch), axis=0)})[0]
            else:
                batch_preds = self.sess.run(self.prediction, feed_dict={self.audio_input: X_batch.reshape(-1, 1, 15, 80, 3), self.other_input: np.repeat(feats_other, len(X_batch), axis=0).reshape(-1, 1, 5)})
            preds.extend(batch_preds.flatten())

        preds = np.array(preds)
        thresh = max(0.1, np.max(preds) * 0.5) if len(preds) > 0 else 0.5
        peaks = argrelextrema(preds, np.greater)[0] if len(preds) > 0 else []
        return librosa.frames_to_time(peaks[preds[peaks] > thresh], sr=sr, hop_length=hop)

def generate_ddc_notes(audio_path, difficulty=3):
    onnx_path = 'lib/models/ddc_onset.onnx'
    tf_ckpt = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/model_sp-56000'

    model_path = onnx_path if os.path.exists(onnx_path) else tf_ckpt
    if not os.path.exists(model_path) and not os.path.exists(model_path + '.index'):
        return generate_fallback_notes(audio_path)

    try:
        print(f"  [DDC-Deep] Using {model_path} for inference...")
        model = DDCInference(model_path)
        onsets = model.predict_onsets(audio_path, difficulty=difficulty)
        if len(onsets) == 0: return generate_fallback_notes(audio_path)

        # Step Selection (Heuristic Flow)
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        if bpm <= 0: bpm = 120.0
        note_16th_dur = 15.0 / bpm
        quantized = np.round(onsets / note_16th_dur).astype(int)
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1
        chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]

        flow_cycle = ["1000", "0100", "0010", "0001"]
        for i, o in enumerate(quantized):
            m_idx, l_idx = o // 16, o % 16
            if m_idx < total_measures: chart_grid[m_idx][l_idx] = flow_cycle[i % 4]
        return ",\n".join(["\n".join(m) for m in chart_grid])
    except Exception as e:
        print(f"Error during ML inference: {e}")
        return generate_fallback_notes(audio_path)

def generate_fallback_notes(audio_path):
    try: y, sr = librosa.load(audio_path, sr=22050)
    except Exception: return "1000\n,\n0001"
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
    if bpm <= 0: bpm = 120.0
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    note_16th_dur = 15.0 / bpm
    quantized = np.unique(np.round(onsets / note_16th_dur).astype(int))
    total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1
    chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
    flow_cycle = ["1000", "0100", "0010", "0001"]
    for i, o in enumerate(quantized):
        m_idx, l_idx = o // 16, o % 16
        if m_idx < total_measures: chart_grid[m_idx][l_idx] = flow_cycle[i % 4]
    return ",\n".join(["\n".join(m) for m in chart_grid])

if __name__ == "__main__":
    diff = 3
    if len(sys.argv) > 2: diff = int(sys.argv[2])
    if len(sys.argv) > 1: print(generate_ddc_notes(sys.argv[1], difficulty=diff))
