import tensorflow as tf
import os
import sys

# DDC uses TF 1.x features
tf.compat.v1.disable_eager_execution()

def convert_v1_to_v2(v1_path, v2_path):
    if not os.path.exists(v1_path):
        print(f"Source {v1_path} not found.")
        return

    print(f"Converting {v1_path} to TF 2.x compatible format...")
    reader = tf.compat.v1.train.NewCheckpointReader(v1_path)
    var_to_shape = reader.get_variable_to_shape_map()

    with tf.compat.v1.Session() as sess:
        new_vars = []
        for var_name in var_to_shape:
            tensor = reader.get_tensor(var_name)
            new_vars.append(tf.compat.v1.Variable(tensor, name=var_name))

        sess.run(tf.compat.v1.global_variables_initializer())
        saver = tf.compat.v1.train.Saver(new_vars)
        saver.save(sess, v2_path)
    print(f"Successfully saved to {v2_path}")

if __name__ == "__main__":
    # Default paths for FCDM
    base = 'bobmania/ArrowVortex/lib/ddc/infer/server_aux/'
    convert_v1_to_v2(base + 'model_sp-56000.v1', base + 'model_sp-56000')
    convert_v1_to_v2(base + 'model_ss-23628.v1', base + 'model_ss-23628')
