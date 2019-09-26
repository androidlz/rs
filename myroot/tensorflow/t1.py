import tensorflow as tf
import os

# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error

graph = tf.Graph()
# 此过程中不能打印变量
with graph.as_default():
    variable = tf.Variable(42, name='foo')
    initialize = tf.compat.v1.global_variables_initializer()
    assign = variable.assign(13)
    matrix1 = tf.constant([[3., 3.]])
    matrix2 = tf.constant([[2.], [2.]])
    product = tf.matmul(matrix1, matrix2)
    print(product)

# 查看并打印变量
with tf.compat.v1.Session(graph=graph) as sess:
    sess.run(initialize)
    sess.run(assign)
    print(sess.run(variable))
    print(sess.run(matrix1))
    print(sess.run(matrix2))
    sess.close()