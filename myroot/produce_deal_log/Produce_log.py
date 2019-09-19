import random

# 制造日志


albet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
albet_num = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '1', '2',
             '3', '4', '5', '6', '7']
albet_Num = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '1', '2',
             '3', '4', '5', '6', '7', 'O', 'P', 'Q', 'R', 'S', 'T']

user_id_list = ['one', 'two', 'three', 'four', 'five', 'six']
'''
1.点击
2.播放
3.点赞
4.收藏
5.付费观看
6.站外分享
7.评论
'''
log_type_list = ['1', '2', '3', '4', '5', '6', '7']

num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
topic_array = ['空气净化器', '净水器', '加湿器', '空气净化滤芯']


def produce():
    file_object = open('./thefile.txt', 'w')
    for i in range(0, 2000):
        cookie = ''.join(random.sample(albet_Num, 10))  # 用''拼接的8个字符
        uid = ''.join(random.sample(user_id_list, 1))
        user_agent = 'Windows Gecko Firefox'
        ip = '192.168.1.100'
        video = ''.join(random.sample(num, 7))
        topic = ''.join(random.sample(topic_array, 1))
        order_id = '0'
        log_type = ''.join(random.sample(log_type_list, 1))
        final = cookie + '&' + uid + "&" + user_agent + "&" + ip + '&' + video + "&" \
                + topic + '&' + order_id + '&' + log_type + '\n'
        print(final)
        file_object.write(final)
    file_object.close()


# produce()

# click_action = {}
# # 读取文件  处理点击日志
# file = open('./thefile.txt')
# for line in file.readlines():
#     line = line.strip()
#     ls = line.split('&')
#     if ls[7] != "1":
#         continue
#     # print(ls[1] + '\t' + ls[4])
#     if ls[1] not in click_action.keys():
#         click_action[ls[1]] = []
#     click_action[ls[1]].append(ls[4])
# for k, v in click_action.items():
#     print(k + '\t' + str(len(v)) + '\t' + '&&'.join(v))

cate_items = {}
# 读取文件  处理点击日志
file = open('./thefile.txt')
for line in file.readlines():
    line = line.strip()
    ls = line.split('&')
    if ls[5] not in cate_items.keys():
        cate_items[ls[5]] = []
    cate_items[ls[5]].append(ls[4])
file_object = open('./cate.log', 'w')
for k, v in cate_items.items():
    line = k + '\t' + '&&'.join(v) + '\n'
    file_object.write(line)


