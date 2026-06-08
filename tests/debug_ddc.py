import os
import sys
import numpy as np
import librosa
import tensorflow as tf
from scripts.ddc_inference import DDCInference

tf.compat.v1.disable_eager_execution()
base = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/'
model = DDCInference(base + 'model_sp-56000', base + 'model_ss-23628')
audio = "itgmania/Songs/StepMania 5/Springtime/Kommisar - Springtime.mp3"

y, sr = librosa.load(audio, sr=44100)
nffts, hop = [1024, 2048, 4096], 512
feat_channels = [librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n, hop_length=hop, n_mels=80, fmin=27.5, fmax=16000), ref=np.max) for n in nffts]
song_feats = np.stack(feat_channels, axis=-1).transpose(1, 0, 2)
padded = np.pad(song_feats, ((7, 7), (0, 0), (0, 0)), mode='constant')

X = np.array([padded[i:i+15] for i in range(100, 150)]).reshape(-1, 1, 15, 80, 3)
other = np.zeros((len(X), 1, 5), dtype=np.float32)
other[:, :, 3] = 1.0

preds = model.sess.run(model.prediction, feed_dict={model.audio_input: X, model.other_input: other})
print(f"Max Pred: {np.max(preds)}")
