""" Simple linear regression example in TensorFlow
This program tries to predict the number of thefts from 
the number of fire in the city of Chicago
Author: Chip Huyen
Prepared for the class CS 20SI: "TensorFlow for Deep Learning Research"
cs20si.stanford.edu
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd

# import utils

DATA_FILE = './fire_theft.xls'
data = []
# Step 1: read in data from the .xls file
for line in open("F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u1.base").readlines():
    user, mid, rating, _ = line.split("\t")
    data.append([user, mid, float(rating)])

# Step 2: create placeholders for input X (number of fire) and label Y (number of theft)
with tf.compat.v1.variable_scope('Inputs'):
    X = tf.compat.v1.placeholder(tf.float32, [1, 2], name='X')
    Y = tf.compat.v1.placeholder(tf.float32, name='Y')
    tf.compat.v1.summary.histogram("X", X)
    tf.compat.v1.summary.histogram("Y", Y)

# Step 3: create weight and bias, initialized to 0
# w = tf.Variable(0.0, name='weights_1')
# u = tf.Variable(0.0,name='weights_2')
# b = tf.Variable(0.0, name='bias')
w = tf.compat.v1.Variable(tf.zeros([2, 1]))
u = tf.compat.v1.Variable(tf.zeros([2, 1]))
b = tf.compat.v1.Variable(0.0)

# Step 4: build model to predict Y
# Y_predicted = X * X * X * w + X * u + b

# Y_predicted = tf.matmul(tf.multiply(X,X),w) + tf.matmul(X,u) + b
# Y_predicted = tf.multiply(X,w) + tf.matmul(X,u) + b
# Y_predicted = tf.matmul(X,w) + b
Y_predicted = tf.matmul(X, w) + b

# Step 5: use the square error as the loss function
# loss = tf.square(Y - Y_predicted, name='loss')
# loss = tf.reduce_mean(tf.square(Y - Y_predicted))
loss = tf.reduce_mean((Y - Y_predicted))
# loss = utils.huber_loss(Y, Y_predicted)
# loss = utils.test_loss(Y, Y_predicted)
# loss = tf.losses.mean_squared_error(Y,Y_predicted)

# Step 6: using gradient descent with learning rate of 0.01 to minimize loss
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.1).minimize(loss)
# optimizer = tf.train.AdadeltaOptimizer(learning_rate=0.01).minimize(loss)

with tf.name_scope("variable"):
    tf.compat.v1.summary.scalar("loss", loss)
    # tf.summary.scalar("y_pred",np.sum(Y_predicted))
    # tf.summary.scalar("y",Y)
    # tf.summary.scalar("w",w)
    # tf.summary.scalar("u",u)
    # tf.summary.scalar("b",b)
with tf.compat.v1.Session() as sess:
    # Step 7: initialize the necessary variables, in this case, w and b
    sess.run(tf.compat.v1.global_variables_initializer())
    writer = tf.compat.v1.summary.FileWriter('./graphs/linear_reg', sess.graph)
    merge_op = tf.compat.v1.summary.merge_all()
    # Step 8: train the model
    sum = 0
    for i in range(100):  # train the model 100 epochs
        total_loss = 0
        for x, y, z in data:
            # print ("x is {},y is {},z is {}".format(x,y,z))
            # Session runs train_op and fetch values of loss
            _, l, mo, y_p, yy, xx = sess.run([optimizer, loss, merge_op, Y_predicted, Y, X],
                                             feed_dict={X: np.array([x, y]).reshape(1, 2), Y: z})
            total_loss += np.sum(l)
            # print ("y_p is {} y is {}".format(y_p,yy))
        sum += total_loss / len(data)
        print('Epoch {0}: {1}'.format(i, total_loss / len(data)))
        writer.add_summary(mo, i)
    print("sum is {0}".format(sum / 100))
    # close the writer when you're done using it
    writer.close()
    # Step 9: output the values of w and b
    # w, b ,u = sess.run([w, b ,u])
# plot the results
