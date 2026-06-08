import os
import sys
import numpy as np
import librosa
try:
    import tensorflow as tf
    tf.compat.v1.disable_eager_execution()
except ImportError:
    tf = None
from scipy.signal import argrelextrema

class DDCInference:
    def __init__(self, sp_ckpt, ss_ckpt):
        self.sp_ckpt, self.ss_ckpt = sp_ckpt, ss_ckpt
        self.sess = tf.compat.v1.Session()
        self._build_sp_model()
        self._build_ss_model()
        self._restore()

    def _build_sp_model(self):
        with tf.compat.v1.variable_scope('model_sp'):
            self.audio_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 15, 80, 3], name='feats_audio')
            self.other_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 5], name='feats_other')
            feats_audio, feats_other = tf.reshape(self.audio_input, shape=[-1, 15, 80, 3]), tf.reshape(self.other_input, shape=[-1, 5])
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

    def _build_ss_model(self):
        with tf.compat.v1.variable_scope('model_ss'):
            self.ss_bag_input = tf.compat.v1.placeholder(tf.float32, shape=[1, 1, 17], name='bag_input')
            self.ss_other_input = tf.compat.v1.placeholder(tf.float32, shape=[1, 1, 2], name='feats_other')
            bag, other = tf.reshape(self.ss_bag_input, [1, 17]), tf.reshape(self.ss_other_input, [1, 2])
            w_proj_sym, w_proj_nosym, b_proj = tf.compat.v1.get_variable('rnn_proj/W', [17, 128]), tf.compat.v1.get_variable('rnn_proj/nosym_W', [2, 128]), tf.compat.v1.get_variable('rnn_proj/b', [128])
            proj = tf.reshape(tf.matmul(bag, w_proj_sym) + tf.matmul(other, w_proj_nosym) + b_proj, [1, 1, 128])
            try:
                cell = tf.compat.v1.nn.rnn_cell.BasicRNNCell(128)
                self.multi_cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([cell] * 2)
                self.state_placeholder = self.multi_cell.zero_state(1, tf.float32)
                outputs, self.next_state = tf.compat.v1.nn.dynamic_rnn(self.multi_cell, proj, initial_state=self.state_placeholder)
                output = tf.reshape(outputs[0], [1, 128])
            except Exception:
                output = tf.reshape(proj, [1, 128])
                self.next_state = None
            sw, sb = tf.compat.v1.get_variable('sym_rnn_output/softmax_w', [128, 257]), tf.compat.v1.get_variable('sym_rnn_output/softmax_b', [257])
            self.ss_probs = tf.nn.softmax(tf.matmul(output, sw) + sb)

    def _restore(self):
        tf.compat.v1.train.Saver(tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope='model_sp')).restore(self.sess, self.sp_ckpt)
        try:
            tf.compat.v1.train.Saver(tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope='model_ss')).restore(self.sess, self.ss_ckpt)
        except Exception: pass

    def predict_onsets(self, audio_path):
        try: y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return np.array([])
        nffts, hop = [1024, 2048, 4096], 512
        feat_channels = [librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000), ref=np.max) for n in nffts]
        song_feats = np.stack(feat_channels, axis=-1).transpose(1, 0, 2)
        padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')
        feats_other = np.zeros((1, 1, 5), dtype=np.float32)
        feats_other[0, 0, 3] = 1.0
        batch_size, preds = 256, []
        for start in range(0, song_feats.shape[0], batch_size):
            end = min(start + batch_size, song_feats.shape[0])
            X_batch = np.array([padded[i:i+15] for i in range(start, end)]).reshape(-1, 1, 15, 80, 3)
            preds.extend(self.sess.run(self.prediction, feed_dict={self.audio_input: X_batch, self.other_input: np.repeat(feats_other, len(X_batch), axis=0)}).flatten())
        peaks = argrelextrema(np.array(preds), np.greater)[0]
        return librosa.frames_to_time(peaks[np.array(preds)[peaks] > 0.5], sr=sr, hop_length=hop)

    def select_steps(self, n_onsets):
        vocab_path = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/labels_4_0123.txt'
        if not os.path.exists(vocab_path): return ["1000"] * n_onsets
        vocab = open(vocab_path).read().splitlines()
        current_bag, other, selected = np.zeros((1, 1, 17), dtype=np.float32), np.zeros((1, 1, 2), dtype=np.float32), []
        current_bag[0, 0, 0], other[0, 0, 0] = 1.0, 1.0
        try: state = self.sess.run(self.state_placeholder)
        except Exception: state = None
        for _ in range(n_onsets):
            if state is not None:
                probs, state = self.sess.run([self.ss_probs, self.next_state], feed_dict={self.ss_bag_input: current_bag, self.ss_other_input: other, self.state_placeholder: state})
            else:
                probs = self.sess.run(self.ss_probs, feed_dict={self.ss_bag_input: current_bag, self.ss_other_input: other})
            idx = np.argmax(probs[0])
            note = vocab[idx]
            selected.append(note)
            current_bag = np.zeros((1, 1, 17), dtype=np.float32)
            if idx == 0: current_bag[0, 0, 0] = 1.0
            else:
                for col in range(4):
                    t = int(note[col])
                    if t > 0: current_bag[0, 0, 1 + (col*4) + (t-1)] = 1.0
        return selected

def generate_ddc_notes(audio_path):
    base = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/'
    sp_ckpt, ss_ckpt = base + 'model_sp-56000', base + 'model_ss-23628'
    if not tf or not os.path.exists(sp_ckpt + '.index'): return generate_fallback_notes(audio_path)
    try:
        model = DDCInference(sp_ckpt, ss_ckpt)
        onsets = model.predict_onsets(audio_path)
        notes = model.select_steps(len(onsets))
        try: y, sr = librosa.load(audio_path, sr=44100)
        except Exception: return "0000\n,\n0000"
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        if bpm <= 0: bpm = 120.0
        note_16th_dur = 15.0 / bpm
        quantized = np.round(onsets / note_16th_dur).astype(int)
        total_measures = (quantized[-1] // 16) + 1 if len(quantized) > 0 else 1
        chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
        for i, o in enumerate(quantized):
            m_idx, l_idx = o // 16, o % 16
            if m_idx < total_measures: chart_grid[m_idx][l_idx] = notes[i]
        return ",\n".join(["\n".join(m) for m in chart_grid])
    except Exception as e:
        print(f"Error: {e}")
        return generate_fallback_notes(audio_path)

def generate_fallback_notes(audio_path):
    try: y, sr = librosa.load(audio_path, sr=22050)
    except Exception: return "0000\n,\n0000"
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
    if len(sys.argv) > 1: print(generate_ddc_notes(sys.argv[1]))
