# encoding=utf-8
import jieba

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

set_list = jieba.cut("苹果新iPhone来了。美国当地时间9月10日上午10时，\
                     苹果在美国加州总部的乔布斯剧院召开秋季产品发布会，推出了三款iPhone，\
                     分别是iPhone 11、iPhone 11 Pro以及iPhone 11 Pro Max")
print(",".join(set_list))
