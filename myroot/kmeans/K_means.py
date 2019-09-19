from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import Birch
import numpy as np
from sklearn import metrics
import time, datetime

# k-Means是基于模型的协同过滤
# X = np.array([[1, 2], [1, 4], [1, 0],
#               [10, 2], [10, 4], [10, 0]])
# y = [1, 1, 1, 0, 0, 0]
# kmeans = KMeans(n_clusters=2, random_state=0).fit(X)  # fit 是训练过程   2是分两类 0和1
# kmeans.labels_
# print(kmeans.predict([[0, 0], [12, 3]]))
# print(kmeans.cluster_centers_)

# 用户对电影的平分 x
# 用户对未来电影的平分 y

u1_base = open('F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u1.base')
X_array = []
Y_array = []
# 用电影划分用户
X_u = []
Y_u = []

# user id | item id | rating | timestamp
'''
聚类算法  1.kmeans
'''
for l in u1_base:
    ls = l.strip().split('\t')
    Y_array.append(int(ls[2]))  # 所有有关于sklearn 机器学习 都要求输入的是整数

    time_local = time.localtime(float(ls[3]))
    dt = time.strftime('%Y/%m/%d', time_local)
    # print(time.strftime("%Y/%m/%d %H:%M:%S", time_local))
    # dt = datetime.datetime.utcfromtimestamp(int(ls[3]))

    month = int(dt.split('/')[1])
    day = int(dt.split('/')[2])
    X_array.append([int(ls[0]), int(ls[1]), month, day])

    X_u.append([ls[1], ls[2]])
    Y_u.append(ls[0])
kmeans = KMeans(n_clusters=5, random_state=1).fit(X_array, Y_array)
# print(kmeans.predict([[1, 1, 874965758]]))

u1_test = open('F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u1.test')
X_array_test = []
# 预测结果
Y_array_test = []

X_u_test = []
Y_u_test = []

for l in u1_test:
    ls = l.strip().split('\t')
    time_local = time.localtime(float(ls[3]))
    dt = time.strftime('%Y/%m/%d', time_local)
    # print(time.strftime("%Y/%m/%d %H:%M:%S", time_local))
    # dt = datetime.datetime.utcfromtimestamp(int(ls[3]))

    month = int(dt.split('/')[1])
    day = int(dt.split('/')[2])
    X_array_test.append([int(ls[0]), int(ls[1]), month, day])

    Y_array_test.append(int(ls[2]))
    X_u_test.append([int(ls[1]), int(ls[2])])
    Y_u_test.append(int(ls[0]))

y_pred = kmeans.predict(X_array_test)
# print(y_pred)
for y in y_pred:
    y += 1
print(metrics.adjusted_rand_score(Y_array_test, y_pred))
# 用电影划分用户
# kmeans_u = KMeans(n_clusters=30, random_state=1).fit(X_u, Y_u)
# y_u_pre = kmeans_u.predict(X_u_test)
# print(metrics.adjusted_rand_score(Y_u_test, y_u_pre))
'''
聚类算法  2.mini batch
'''
mini_batch = MiniBatchKMeans(n_clusters=5, random_state=0,
                             batch_size=20000, ).fit(X_array, Y_array)
y_mini_pred = mini_batch.predict(X_array_test)
print(metrics.adjusted_rand_score(Y_array_test, y_mini_pred))
'''
聚类算法  3.birch
'''
brc = Birch(branching_factor=5, n_clusters=None, threshold=0.5, compute_labels=True).fit(X_array[:10000],
                                                                                         Y_array[:10000])
y_bi_pre = brc.predict(X_array_test)
print(metrics.adjusted_rand_score(Y_array_test, y_bi_pre))
