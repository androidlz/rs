import tensorflow as tf
import os
import numpy as np

# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息
from numpy.core.tests.test_mem_overlap import xrange

from myroot.tensorflow.t2 import output, in1, in2

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error

# 曲线拟合
x_data = np.random.rand(100).astype('float32')
# wx+b=y        w=0.1    b=0.3(防止过拟合)
y_data = x_data * 0.1 + 0.3

W = tf.Variable(tf.random.uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))

y = W * x_data + b

# 损失函数
loss = tf.reduce_mean(tf.square(y - y_data))
# 找到最低点
optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.5)
# 保证loss是最小的
train = optimizer.minimize(loss)
# 初始化Tensorflow参数
init = tf.compat.v1.global_variables_initializer()

# 运行数据流图
sess = tf.compat.v1.Session()
sess.run(init)

sum = 0
for step in xrange(201):
    sess.run(train)
    l = sess.run([loss])
    print("loss == %s,%s" % (l, W))
    sum += sess.run(loss)
    # if step % 20 == 0:
    #     print(step, sess.run(W), sess.run(b), sess.run(loss))
    print(sum / 201)
