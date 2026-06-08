import tensorflow as tf
import os
import sys

# DDC uses TF 1.x features
tf.compat.v1.disable_eager_execution()

def convert_sp(v1_path, v2_path):
    if not os.path.exists(v1_path): return
    print(f"Converting SP: {v1_path}...")
    reader = tf.compat.v1.train.NewCheckpointReader(v1_path)
    var_to_shape = reader.get_variable_to_shape_map()
    with tf.compat.v1.Session() as sess:
        new_vars = [tf.compat.v1.Variable(reader.get_tensor(v), name=v) for v in var_to_shape]
        sess.run(tf.compat.v1.global_variables_initializer())
        tf.compat.v1.train.Saver(new_vars).save(sess, v2_path)

def convert_ss(v1_path, v2_path):
    if not os.path.exists(v1_path): return
    print(f"Converting SS: {v1_path}...")
    reader = tf.compat.v1.train.NewCheckpointReader(v1_path)
    # Map old names to new LSTM naming
    mapping = {
        'model_ss/rnn_unroll/MultiRNNCell/Cell0/BasicLSTMCell/Linear/Matrix': 'model_ss/Cell0/lstm_cell/kernel',
        'model_ss/rnn_unroll/MultiRNNCell/Cell0/BasicLSTMCell/Linear/Bias': 'model_ss/Cell0/lstm_cell/bias',
        'model_ss/rnn_unroll/MultiRNNCell/Cell1/BasicLSTMCell/Linear/Matrix': 'model_ss/Cell1/lstm_cell/kernel',
        'model_ss/rnn_unroll/MultiRNNCell/Cell1/BasicLSTMCell/Linear/Bias': 'model_ss/Cell1/lstm_cell/bias',
    }
    with tf.compat.v1.Session() as sess:
        new_vars = []
        for old_v in reader.get_variable_to_shape_map():
            new_name = mapping.get(old_v, old_v)
            new_vars.append(tf.compat.v1.Variable(reader.get_tensor(old_v), name=new_name))
        sess.run(tf.compat.v1.global_variables_initializer())
        tf.compat.v1.train.Saver(new_vars).save(sess, v2_path)

if __name__ == "__main__":
    base = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/'
    convert_sp(base + 'model_sp-56000.v1', base + 'model_sp-56000')
    convert_ss(base + 'model_ss-23628.v1', base + 'model_ss-23628')
