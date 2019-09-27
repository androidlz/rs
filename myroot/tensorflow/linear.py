import tensorflow as tf
import numpy as np
import xlrd
import matplotlib.pyplot as plt
import os

# os.environ["TF_CPP_MIN_LOG_LEVEL"]='1' # 这是默认的显示等级，显示所有信息
from statsmodels.tsa.tests.results.results_arma import Y_arma02

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error
# os.environ["TF_CPP_MIN_LOG_LEVEL"]='3' # 只显示 Error

# 寻找芝加哥 着火数和偷窃数之间的关系
DATA_FILE = 'fire_theft.xls'

# 1.read from data file
book = xlrd.open_workbook(DATA_FILE, encoding_override="utf-8")
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])
n_samples = sheet.nrows - 1

# 2.creat placeholders for input x(number of file) and label Y(number of theft)
# 发生火灾的数量
X = tf.compat.v1.placeholder(tf.float32, name='X')
# 发生盗窃的数量
Y = tf.compat.v1.placeholder(tf.float32, name='Y')

# 3.creat weight and bias ,init to 0
w = tf.Variable(0.0, name='weights')
b = tf.Variable(0.0, name='bias')

# 4.build model to predict Y
Y_predicted = X * w + b

# 5.use square error as the lose function
# loss = tf.square(Y - Y_predicted, name='loss')
# loss = tf.compat.v1.losses.huber_loss(Y, Y_predicted)
# loss = tf.losses.softmax_cross_entropy(Y, Y_predicted)
loss = tf.compat.v1.losses.log_loss(Y, Y_predicted)
# loss = utils.huber_loss(Y,Y_predicted)

# 6.using gradient descent with learning rate 0.01 to minimize loss
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)

with tf.compat.v1.Session() as sess:
    # 7.init necessary variables (w and b)
    sess.run(tf.compat.v1.global_variables_initializer())

    writer = tf.compat.v1.summary.FileWriter('./my_graph/linear_reg', sess.graph)

    # 8.train the model 100 times
    for i in range(100):
        total_loss = 0
        for x, y in data:
            # session runs train_op and fetch values of loss
            _, l = sess.run([optimizer, loss], feed_dict={X: x, Y: y})
            total_loss += l
        print('Epoch {0}:{1}'.format(i, total_loss / n_samples))

    # close the writer
    writer.close()

    # 9.output the value of w and b
    w_value, b_value = sess.run([w, b])

# plot the result
X, Y = data.T[0], data.T[1]
plt.plot(X, Y, 'bo', label='Real data')
plt.plot(X, X * w_value + b_value, 'r', label='Predected data')
plt.legend()
plt.show()
