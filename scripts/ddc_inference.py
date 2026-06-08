import os
import sys
import numpy as np
import librosa
import tensorflow as tf
from scipy.signal import argrelextrema

# DDC uses TF 1.x features
tf.compat.v1.disable_eager_execution()

class DDCInference:
    def __init__(self, sp_ckpt):
        self.sp_ckpt = sp_ckpt
        self.sess = tf.compat.v1.Session()
        self._build_model()
        self._restore()

    def _build_model(self):
        with tf.compat.v1.variable_scope('model_sp'):
            self.audio_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 15, 80, 3], name='feats_audio')
            self.other_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 1, 5], name='feats_other')

            feats_audio = tf.reshape(self.audio_input, shape=[-1, 15, 80, 3])
            feats_other = tf.reshape(self.other_input, shape=[-1, 5])

            w0 = tf.compat.v1.get_variable('cnn_0/filters', [7, 3, 3, 10])
            b0 = tf.compat.v1.get_variable('cnn_0/biases', [10])
            conv0 = tf.nn.conv2d(feats_audio, w0, [1, 1, 1, 1], padding='VALID')
            relu0 = tf.nn.relu(tf.nn.bias_add(conv0, b0))
            pool0 = tf.nn.max_pool2d(relu0, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')

            w1 = tf.compat.v1.get_variable('cnn_1/filters', [3, 3, 10, 20])
            b1 = tf.compat.v1.get_variable('cnn_1/biases', [20])
            conv1 = tf.nn.conv2d(pool0, w1, [1, 1, 1, 1], padding='VALID')
            relu1 = tf.nn.relu(tf.nn.bias_add(conv1, b1))
            pool1 = tf.nn.max_pool2d(relu1, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')

            flat_cnn = tf.reshape(pool1, [-1, 1120])
            feats_all = tf.concat([flat_cnn, feats_other], axis=1)

            wd0 = tf.compat.v1.get_variable('dnn_0/W', [1125, 256])
            bd0 = tf.compat.v1.get_variable('dnn_0/b', [256])
            dnn0 = tf.nn.relu(tf.matmul(feats_all, wd0) + bd0)

            wd1 = tf.compat.v1.get_variable('dnn_1/W', [256, 128])
            bd1 = tf.compat.v1.get_variable('dnn_1/b', [128])
            dnn1 = tf.nn.relu(tf.matmul(dnn0, wd1) + bd1)

            wl = tf.compat.v1.get_variable('logit/W', [128, 1])
            bl = tf.compat.v1.get_variable('logit/b', [1])
            self.logits = tf.matmul(dnn1, wl) + bl
            self.prediction = tf.nn.sigmoid(self.logits)

    def _restore(self):
        vars_to_restore = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.GLOBAL_VARIABLES, scope='model_sp')
        saver = tf.compat.v1.train.Saver(vars_to_restore)
        saver.restore(self.sess, self.sp_ckpt)

    def predict_onsets(self, audio_path):
        y, sr = librosa.load(audio_path, sr=44100)
        nffts = [1024, 2048, 4096]
        hop = 512
        feat_channels = []
        for nfft in nffts:
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=nfft, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000)
            log_S = librosa.power_to_db(S, ref=np.max)
            feat_channels.append(log_S)

        # [Channels, Bands, Frames] -> [Frames, Bands, Channels]
        song_feats = np.stack(feat_channels, axis=-1).transpose(1, 0, 2)

        n_frames = song_feats.shape[0]
        padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')

        feats_other = np.zeros((1, 1, 5), dtype=np.float32)
        feats_other[0, 0, 3] = 1.0

        batch_size = 256
        preds = []
        for start in range(0, n_frames, batch_size):
            end = min(start + batch_size, n_frames)
            X_batch = []
            for i in range(start, end):
                X_batch.append(padded[i:i+15])
            X_batch = np.array(X_batch).reshape(-1, 1, 15, 80, 3)
            feed_dict = {
                self.audio_input: X_batch,
                self.other_input: np.repeat(feats_other, len(X_batch), axis=0)
            }
            batch_preds = self.sess.run(self.prediction, feed_dict=feed_dict)
            preds.extend(batch_preds.flatten())

        preds = np.array(preds)
        peaks = argrelextrema(preds, np.greater)[0]
        onsets_idx = peaks[preds[peaks] > 0.5]
        onsets_times = librosa.frames_to_time(onsets_idx, sr=sr, hop_length=hop)
        return onsets_times, preds

def generate_ddc_notes(audio_path):
    sp_ckpt = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/model_sp-56000'
    if not os.path.exists(sp_ckpt + '.index'):
        return generate_fallback_notes(audio_path)

    try:
        model = DDCInference(sp_ckpt)
        onsets, _ = model.predict_onsets(audio_path)
        y, sr = librosa.load(audio_path, sr=44100)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
        if bpm <= 0: bpm = 120.0
        note_16th_dur = 15.0 / bpm
        unique_onsets = np.unique(np.round(onsets / note_16th_dur).astype(int))
        max_16th = unique_onsets[-1] if len(unique_onsets) > 0 else 0
        total_measures = (max_16th // 16) + 1
        chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
        flow_cycle = ["1000", "0100", "0010", "0001"]
        flow_idx = 0
        for o in unique_onsets:
            m_idx, l_idx = o // 16, o % 16
            if m_idx < total_measures:
                chart_grid[m_idx][l_idx] = flow_cycle[flow_idx]
                flow_idx = (flow_idx + 1) % len(flow_cycle)
        return ",\n".join(["\n".join(m) for m in chart_grid])
    except Exception as e:
        print(f"Error: {e}")
        return generate_fallback_notes(audio_path)

def generate_fallback_notes(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
    if bpm <= 0: bpm = 120.0
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    note_16th_dur = 15.0 / bpm
    unique_onsets = np.unique(np.round(onsets / note_16th_dur).astype(int))
    max_16th = unique_onsets[-1] if len(unique_onsets) > 0 else 0
    total_measures = (max_16th // 16) + 1
    chart_grid = [["0000" for _ in range(16)] for _ in range(total_measures)]
    flow_cycle = ["1000", "0100", "0010", "0001"]
    flow_idx = 0
    for o in unique_onsets:
        m_idx, l_idx = o // 16, o % 16
        if m_idx < total_measures:
            chart_grid[m_idx][l_idx] = flow_cycle[flow_idx]
            flow_idx = (flow_idx + 1) % len(flow_cycle)
    return ",\n".join(["\n".join(m) for m in chart_grid])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_ddc_notes(sys.argv[1]))
