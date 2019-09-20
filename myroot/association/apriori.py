# apriori 算法
# 1.产生频繁集
#       （1）最小支持过滤
#       （2）apriori函数
#              loadDataSet   creatC1   aprioriGen   scanD
# 2.产生关联规则
#       （1）最小置信度过滤
#       （2）generateRule函数
#               rulesFromConseq函数  生成候选规则集
#               calcConf函数   用最小置信度


# 生成原始数据  用于测试
def loadDataSet():
    return [[1, 3, 4],
            [2, 3, 5],
            [1, 2, 3, 5],
            [2, 5]]


# 创建C1：单个元素的集合
def createC1(dataSet):
    '''
    [frozenset({1}),
     frozenset({2}),
     frozenset({3}),
     frozenset({4}),
     frozenset({5})]
    '''
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))


# 统计支持度并且过滤，C1-->L1
def scanD(D, Ck, minSupport):
    ssCnt = {}

    # 统计每个候选集出现在记录中的个数
    for tid in D:  # 遍历每一个记录
        for can in Ck:  # 遍历候选集
            if can.issubset(tid):  # 若候选集在记录中
                ssCnt[can] = ssCnt.get(can, 0) + 1

    # 计算支持度
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:  # 遍历每一个候选集
        support = ssCnt[key] / numItems  # 计算该候选集的支持度

        # 过滤,只保留大于支持率的候选集
        if support >= minSupport:
            retList.insert(0, key)  # 在首部插入
        supportData[key] = support
    return retList, supportData


dataSet = loadDataSet()
C1 = createC1(dataSet)
L1, supportData0 = scanD(dataSet, C1, 0.5)
L1


# 完整的Apriori算法

# Lk-1 --> Ck：组合
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):  # 第一个元素
        L1 = list(Lk[i])[:k - 2]  # 左闭右开
        L1.sort()
        for j in range(i + 1, lenLk):  # 第二个元素
            L2 = list(Lk[j])[:k - 2]
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


# Apriori主函数
def apriori(dataSet, minSupport=0.5):
    # 创建C1-->L1
    C1 = createC1(dataSet)
    D = list(map(set, dataSet))  # 所有数据
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2

    # Ck-->Lk：过滤
    while (len(L[k - 2]) > 0):  # 直到最后的元素为空则停止
        Ck = aprioriGen(L[k - 2], k)  # k-2:从index=0开始
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


# 生成关联规则
# 输入：apriori函数生成频繁项集合列表L，支持度列表、最小置信度
# 输入包含可信度规则的列表
# 作用：产生关联规则
def generateRules(L, supportData, minConf=0.7):
    # 执行度规则列表，最后返回
    bigRuleList = []
    # L0为频繁1-项集
    # 无法从1-项集中构造关联规则，所以从2-项集开始遍历L中每一个频繁项集
    for i in range(1, len(L)):  # 从包含两个元素的项集开始，因为单个元素没有其他元素与之关联
        for freqSet in L[i]:
            '''
            遍历L层;
                    [[frozenset({1}), frozenset({3}), frozenset({2}), frozenset({5})],
                     [frozenset({3, 5}), frozenset({1, 3}), frozenset({2, 5}), frozenset({2, 3})],
                     [frozenset({2, 3, 5})],
                     []]
            L0：项集一个元素；
            L1：项集两个元素;
            L2：项集三个元素
            '''
            H1 = [frozenset([item]) for item in freqSet]  # 收集一个项集的关联规则的右边
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:  # 右边只有一个元素，直接计算可信度
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


# 计算可信度
def calcConf(freqSet, H, supportData, brList, minConf=0.7):
    '''
    freqSet:frozenset({3, 5})
    H:[frozenset({3}), frozenset({5})]
    frozenset({5}) --> frozenset({3}) conf: 0.6666666666666666
    frozenset({3}) --> frozenset({5}) conf: 0.6666666666666666
    '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brList.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)  # 剪枝之后的右边
    return prunedH


def rulesFromConseq(freqSet, H, supportData, brList, minConf=0.7):
    #     print(freqSet) #frozenset({2, 3, 5})
    #     print(H) #[frozenset({2}), frozenset({3}), frozenset({5})]
    m = len(H[0])  # 1
    if (len(freqSet) > (m + 1)):  # m+1表示左边一个，右边m个，len(freqSet)就是总的项集元素个数
        Hmp1 = aprioriGen(H, m + 1)  # 合并，规则进行组合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brList, minConf)
        if (len(Hmp1) > 1):  # 如果不止一条规则满足要求，则考虑进一步合并
            rulesFromConseq(freqSet, Hmp1, supportData, brList, minConf)


if __name__ == '__main__':
    dataSet = loadDataSet()
    L, supportData = apriori(dataSet, minSupport=0.5)
    print("LLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    print(L)
    rules = generateRules(L, supportData, minConf=0.5)
    print('rules-----------------------')
    print(rules)
