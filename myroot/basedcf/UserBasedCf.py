import math
from scipy.spatial import distance
import numpy as np

'''
性能：计算用户相似矩阵的代价很大，适用于用户较少场合
1.根据不同用户对相同商品或内容的偏好程度计算用户之间的相似度
2.在有相同喜好的用户间进行商品推荐
'''


class UserBasedCF:
    def __init__(self, train_file, test_file):
        self.train_file = train_file
        self.test_file = test_file
        self.readData()
        self.UserSimilarity()

    def readData(self):
        self.train = dict()
        train_file = open(self.train_file)
        for line in train_file:
            user, item, score, _ = line.strip().split('\t')
            self.train.setdefault(user, {})
            self.train[user][item] = int(score)
        self.test = dict()
        test_file = open(self.test_file)
        for line in test_file:
            user, item, score, _ = line.strip().split('\t')
            self.test.setdefault(user, {})
            self.test[user][item] = int(score)

    # 计算用户之间的相似度
    def UserSimilarity(self):
        # 物品-用户矩阵
        self.item_users = dict()

        for user, items in self.train.items():
            for i in items.keys():
                if i not in self.item_users:
                    self.item_users[i] = set()
                self.item_users[i].add(user)
        C = dict()  # 用户-用户的共现矩阵
        N = dict()  # 用户购买相同物品的次数
        Cor = dict()
        for i, users in self.item_users.items():
            for u in users:
                N.setdefault(u, 0)
                N[u] += 1

                C.setdefault(u, {})
                for v in users:
                    if u == v:
                        continue
                    C[u].setdefault(v, 0)
                    # 找共现矩阵
                    C[u][v] += 1
                Cor.setdefault(u, [])
                for v in user:
                    if u == v:
                        continue
                    Cor[u].append(v)
        self.W = dict()
        self.Euc = dict()
        self.Cos = dict()
        self.Man = dict()
        # 遍历共现矩阵

        for u, related_users in C.items():
            self.W.setdefault(u, {})
            self.Euc.setdefault(u, {})
            self.Cos.setdefault(u, {})
            self.Man.setdefault(u, {})
            for v, cuv in related_users.items():
                # 相似度计算公式
                # self.W[u][v] = cuv / (math.sqrt(N[u] * N[v]))
                if u in Cor.keys() and v in Cor.keys():
                    # 欧式距离  离得越远越不相关
                    # self.Euc[u][v] = distance.cdist([Cor[u][:10]], [Cor[v][:10]], 'euclidean')
                    print(distance.cdist([Cor[u][:10]], [Cor[v][:10]], 'euclidean'))

                    # cosine
                    # self.Cos[u][v] = np.sum(distance.cdist([Cor[u][:10]], [Cor[v][:10]], 'cosine'))
                    # 曼哈顿距离
                    # self.Man[u][v] = np.sum(distance.cdist([Cor[u][:10]], [Cor[v][:10]], 'cityblock'))
                    # print(self.Euc[u][v])
                    # print(self.Cos[u][v])
                    # print(self.Man[u][v])
                    print('--------------------')
        return self.W

    def Recommend(self, user, K=3, N=10):
        rank = dict()
        action_item = self.train[user].keys()
        # wuv 是v用户和其他所有用户之间的相似度
        for v, wuv in sorted(self.W[user].items(), key=lambda x: x[1], reverse=True)[0:K]:
            # 取出相似度最相关的前三个   i是商品的key   rvi和我相似的用户对商品的评分
            for i, rvi in self.train[v].items():
                if i in action_item:
                    continue
                rank.setdefault(i, 0)
                rank[i] += wuv * rvi  # 我对人的相似程度*相似用户对商品的评分
        # 返回的是商品列表
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]


if __name__ == '__main__':
    cf = UserBasedCF('F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u.data',
                     'F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u.data')
    print(cf.Recommend('3'))
