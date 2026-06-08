import tensorflow as tf
import tf2onnx
import onnx
import os
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

tf.compat.v1.disable_eager_execution()

def export_sp_to_onnx(ckpt_path, onnx_path):
    print(f"Exporting {ckpt_path} to ONNX...")
    tf.compat.v1.reset_default_graph()
    with tf.compat.v1.Session() as sess:
        audio_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 15, 80, 3], name='audio_input')
        other_input = tf.compat.v1.placeholder(tf.float32, shape=[None, 5], name='other_input')

        with tf.compat.v1.variable_scope('model_sp'):
            w0 = tf.compat.v1.get_variable('cnn_0/filters', [7, 3, 3, 10])
            b0 = tf.compat.v1.get_variable('cnn_0/biases', [10])
            conv0 = tf.nn.conv2d(audio_input, w0, [1, 1, 1, 1], padding='VALID')
            relu0 = tf.nn.relu(tf.nn.bias_add(conv0, b0))
            pool0 = tf.nn.max_pool2d(relu0, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')

            w1 = tf.compat.v1.get_variable('cnn_1/filters', [3, 3, 10, 20])
            b1 = tf.compat.v1.get_variable('cnn_1/biases', [20])
            conv1 = tf.nn.conv2d(pool0, w1, [1, 1, 1, 1], padding='VALID')
            relu1 = tf.nn.relu(tf.nn.bias_add(conv1, b1))
            pool1 = tf.nn.max_pool2d(relu1, ksize=[1, 1, 3, 1], strides=[1, 1, 3, 1], padding='SAME')

            flat = tf.reshape(pool1, [-1, 1120])
            feats_all = tf.concat([flat, other_input], axis=1)

            wd0 = tf.compat.v1.get_variable('dnn_0/W', [1125, 256])
            bd0 = tf.compat.v1.get_variable('dnn_0/b', [256])
            dnn0 = tf.nn.relu(tf.matmul(feats_all, wd0) + bd0)

            wd1 = tf.compat.v1.get_variable('dnn_1/W', [256, 128])
            bd1 = tf.compat.v1.get_variable('dnn_1/b', [128])
            dnn1 = tf.nn.relu(tf.matmul(dnn0, wd1) + bd1)

            wl = tf.compat.v1.get_variable('logit/W', [128, 1])
            bl = tf.compat.v1.get_variable('logit/b', [1])
            output = tf.nn.sigmoid(tf.matmul(dnn1, wl) + bl, name='output_node')

        saver = tf.compat.v1.train.Saver()
        saver.restore(sess, ckpt_path)

        # Freeze graph
        output_graph_def = tf.compat.v1.graph_util.convert_variables_to_constants(
            sess, sess.graph_def, ['model_sp/output_node'])

        with tf.Graph().as_default() as g:
            tf.import_graph_def(output_graph_def, name="")
            onnx_graph = tf2onnx.tfonnx.process_tf_graph(g, input_names=['audio_input:0', 'other_input:0'], output_names=['model_sp/output_node:0'])
            model_proto = onnx_graph.make_model("DDC_Onset")
            with open(onnx_path, "wb") as f:
                f.write(model_proto.SerializeToString())

    print(f"ONNX model saved to {onnx_path}")

if __name__ == "__main__":
    ckpt = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/model_sp-56000'
    out = 'lib/models/ddc_onset.onnx'
    os.makedirs('lib/models', exist_ok=True)
    export_sp_to_onnx(ckpt, out)
