import tensorflow as tf
import os

# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error

state = tf.Variable(0, name="counter")
one = tf.constant(1)
new_value = tf.add(state, one)
update = tf.compat.v1.assign(state, new_value)

init_op = tf.compat.v1.global_variables_initializer()

input1 = tf.constant(3.0)
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)

intermed = tf.add(input2, input3)
mul = tf.multiply(input1, intermed)

# 填充
in1 = tf.compat.v1.placeholder(tf.float32)
in2 = tf.compat.v1.placeholder(tf.float32)
output = tf.multiply(in1, in2)

# 抓取
with tf.compat.v1.Session() as sess:
    sess.run(init_op)
    print(sess.run(state))
    for i in range(3):
        pass
        sess.run(update)
        print(sess.run(state))
    # print(sess.run([mul, intermed]))
    print(sess.run([output], feed_dict={in1: [7.], in2: [2.]}))
