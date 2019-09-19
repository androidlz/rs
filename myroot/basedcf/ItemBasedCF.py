import math
from operator import itemgetter

'''
性能：适用物品数明显小于用户数的场合（预算不足的情况）
1.计算物品之间的相似度
2.根据物品之间的相似度和用户历史行为给用户生成推荐列表
'''
# 基于物品的协同过滤
class ItemBasedCF:
    def __init__(self, train_file, test_file):
        # 训练数据
        self.train_file = train_file
        # 测试数据
        self.test_file = test_file
        self.readData()

    # 数据读取函数  生成用户-物品的评分表和测试表
    def readData(self):
        # 训练集
        self.train = dict()
        # 读取训练数据
        train_file = open(self.train_file)
        for line in train_file:
            # 获得用户、物品、评分数据，丢弃时间数据
            user, item, score, _ = line.strip().split('\t')
            # 用户物品评分矩阵
            self.train.setdefault(user, {})
            # 分数赋值
            self.train[user][item] = int(score)
        # 测试集
        self.test = dict()
        # 打开文件 按行读取训练数据
        test_file = open(self.test_file)
        for line in test_file:
            user, item, score, _ = line.strip().split('\t')
            # 用户物品评分矩阵
            self.test.setdefault(user, {})
            # 分数赋值
            self.test[user][item] = int(score)

    # 计算物品之间的相似度   建立物品-物品之间的共现矩阵
    def ItemSimilarity(self):
        C = dict()  # 物品-物品的共现矩阵
        N = dict()  # 物品被多少个不同用户购买
        # 遍历训练数据，获得用户对有过行为的物品
        for user, items in self.train.items():
            # 遍历用户每个物品项
            for i in items.keys():
                N.setdefault(i, 0)
                # 该物品被用户购买  计数加1
                N[i] += 1
                C.setdefault(i, {})
                # 遍历该用户每件物品项
                for j in items.keys():
                    # 若为当前物品，跳过（计算相同商品的相似度没意义）
                    if i == j:
                        continue
                    # 同一用户下，其他物品项，遍历到其他不同物品则加1  初始化为0
                    C[i].setdefault(j, 0)
                    # 找共现矩阵
                    C[i][j] += 1
        # 计算相似度矩阵
        # 计算物品-物品之间的相似度，余弦相似度
        self.W = dict()
        # 遍历物品-物品共现矩阵的所有项，每行物品、该行下的其他物品
        for i, related_items in C.items():
            # 存放物品间的相似度
            self.W.setdefault(i, {})
            # 遍历每一个物品以及对应的同线矩阵的值
            for j, cij in related_items.items():
                # 余弦相似度计算公式
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        # 返回物品相似度
        return self.W

    # 给用户user推荐，前K个相关用户喜欢的，用户user未产生过行为的物品
    # 默认3个用户，推荐10个商品
    def Recommend(self, user, K=3, N=10):
        # 用户user对物品的偏好值
        rank = dict()
        # 用户user产生过行为的物品项item和平分
        action_item = self.train[user]

        # 找到用户user产生过行为的物品item与物品item按相似度从大到小排列，取与物品item相似度最大的K个物品
        for item, score in action_item.items():
            # 取出相似度最相关的前三个  遍历与物品最相似的前K个物品，获得这些物品及相似分数
            for j, wj in sorted(self.W[item].items(), key=lambda x: x[1], reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                # 计算用户user对物品i的偏好值，初始化为0
                rank.setdefault(j, 0)
                # 通过与其相似物品对物品i的偏好值相乘并相加
                rank[j] += score * wj

        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]


if __name__ == '__main__':
    cf = ItemBasedCF('F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u.data',
                     'F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u.data')
    cf.ItemSimilarity()
    print(cf.Recommend('3'))
