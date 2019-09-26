# -*- coding: utf-8 -*-
import socket

# from myroot.produce_deal_log.Data_P2 import r2

HOST, PORT = socket.gethostname(), 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving Http on port %s' + str(PORT))


def Processing(request):
    uid = request.split('keys=')[1].split('')[0]


def gp(uid):
    click_action = {}
    file = open("./thefile.txt", 'r')
    for line in file.readlines():
        line = line.strip()
        ls = line.split('&')
        if ls[7] != "1":
            continue
        if ls[1] not in click_action.keys():
            click_action[ls[1]] = []
        click_action[ls[1]].append(ls[4])
    if uid in click_action.keys():
        return "&&".join(click_action[uid])
    return


# class Rec:
#     def process(self, request):
#         uid = request.split('keys=')[1].split('')[0]
#         return self.rec(uid)
#
#     def rec(self, uid):
#         rec = 'hello world'
#         return rec
#
#
# r = Rec()

comment_log = {}  # key   uid   value  video_ids


def log_process(request):
    print(" xiao  ming log")
    print(request)
    print(type(request))
    print(type(request.decode()))
    request = request.decode().strip()
    ls = request.split('&')
    if ls[1] not in comment_log.keys():
        comment_log[ls[1]] = []
    comment_log[ls[1]].append(ls[4])
    for k, v in comment_log.items():
        print(k + '\t' + '&&'.join(v))
    return 'yes got it'


# 请求的预处理
file = open('./cate.log')
cate_items = {}
for line in file.readlines():
    line = line.strip()
    ls = line.split('\t')
    if ls[0] not in cate_items.keys():
        cate_items[ls[0]] = []
    lss = ls[1].split('&&')
    for v in lss:
        cate_items[ls[0]].append(v)


# print('pre process log')
# for k, v in cate_items.items():
# print(k + '\t' + '&&'.join(v))


# request请求的结果
def log_process_one(request, tag):
    # tag=1 文字 返回与文字相匹配的商品
    # tag=2 数字 返回与数字相同类型目的商品
    if tag == 1:
        if request in cate_items.keys():
            return '&&'.join(cate_items[request])
        else:
            return 'wrong request'
    elif tag == 2:
        for k, v in cate_items.items():
            if request in v:
                # 人工干预个性化推荐
                # return request + "#specal#" + '&&'.join(v)
                return v[0] + "&&" + request + "#specal#" + '&&'.join(v[1:])
        return 'wrong request'
        pass
    else:
        return 'wrong'


class CutIndex:
    cut = {}

    def __init__(self):
        file = open('./index_cut_1.txt')
        for line in file.readlines():
            ls = line.split('\t')
            if ls[0] + '#' + ls[1] not in self.cut.keys():
                self.cut[ls[0] + '#' + ls[1]] = int(ls[2].strip())
            else:
                self.cut[ls[0] + '#' + ls[1]] += v
            print(line)
        pass

    # 读文件
    def read(self, key):
        for k, v in self.cut.items():
            if 'filename :1' + '#' + key == k:
                return 'filename :1'
            elif 'filename :2' + '#' + key == k:
                return 'filename :2'
            elif 'filename :3' + '#' + key == k:
                return 'filename :3'
            elif 'filename :4' + '#' + key == k:
                return 'filename :4'
            else:
                return "not found "


# Real time ranking 实时排序
class RTR:
    old = ['1', '2', '3', '4', '5']
    new = ['5', '4', '3', '2', '1']

    # def __init__(self):
    #     pass

    def p(self, key):
        # m = r2.get('9527#1')
        if m != None:
            if int(m) > 5000:
                return 'more than 5000'
            else:
                return 'less than 5000'
            return ','.join(self.new)
        else:
            return ','.join(self.old)


class Movie:
    movie = {}
    related = {}
    related_fp = {}

    def __init__(self):
        file = open('F:/推荐系统算法/大数据/代码/推荐系统算法工程师-代码/代码/ml-100k/u.item', encoding='utf-8')
        for line in file.readlines():
            # ls=line.encode('utf-8').split('|')
            ls = line.split('|')
            self.movie[ls[0]] = '&&'.join(ls[1:])
        # file = open('./result_apriori')
        # for line in file.readlines():
        #     ls = line.split("&&")
        #     self.related[ls[0]] = "&&".join(ls[1:])
        file = open('./result_fpGrowth')
        for line in file.readlines():
            ls = line.strip().split("&&")
            self.related_fp[ls[0]] = "&&".join(ls[1:])

    def check(self, movieId):
        # movie id | movie title | release date | video release date | IMDb URL | unknown | Action |
        # Adventure | Animation | Children 's | Comedy | Crime | Documentary | Drama | Fantasy |
        # Film - Noir | Horror | Musical | Mystery | Romance | Sci - Fi | Thriller | War | Western |

        if movieId in self.movie.keys():
            m = self.movie[movieId].split('&&')
            ret = ""
            for i in range(0, len(m)):
                if i < 3:
                    ret += m[i]
                    ret += "\t"
                # 判断3位置是否是动作电影，以此类推4,5......
                if i == 3:
                    if m[i] == "0":
                        ret += 'no action'
                        ret += "\t"
                    else:
                        ret += "action"
                        ret += "\t"
                if i == 4:
                    if m[i] == "0":
                        ret += 'no Adventure'
                        ret += "\t"
                    else:
                        ret += "Adventure"
                        ret += "\t"
                print(i)
        return ret

    def find_related(self, movieId):
        if movieId in self.related[movieId]:
            return self.related[movieId]
        return 'not found'

    def detail(self, movied):
        ret = ""
        if movied in self.related.keys():
            ids = self.related[movied].split("&&")
            for idss in ids:
                ret += self.check(idss)
                ret += '\r\n'
        return ret

    def detail_fp(self, movied):
        ret = ''
        if movied in self.related_fp.keys():
            ids = self.related_fp[movied].split("&&")
            for idss in ids:
                ret += self.check(idss)
                ret += '\r\n'
        return ret


while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    # http_response = gp(request)
    print(request)
    # Processing(request)
    # r.process(request)
    # http_response = """
    #             HTTP/1.1 200 OK
    #             first one
    #             first one
    #             """
    paras, tag = request.decode().strip('EOF').split("&&")
    # real time ranking实时排序
    # r = RTR()
    # http_response = r.p(paras)

    m = Movie()
    # http_response = m.check(paras)
    # http_response = m.find_related(paras)
    # http_response = m.detail(paras)
    http_response = m.detail_fp(paras)

    # 返回文件名
    # c = CutIndex()
    # http_response = c.read(paras)

    # http_response = log_process_one(paras, int(tag))
    client_connection.sendall(http_response.encode())
    client_connection.close()

# import socket
#
# host = socket.gethostname()
# port = 12347
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((host, port))
# s.listen(1)
# sock, addr = s.accept()
# print('Connection built')
# info = ''
# while True:
#     info = sock.recv(1024).decode()
#     print('receive:' + info)
#     send_mes = raw_input("send:")
#     sock.send(send_mes.encode())
#     if send_mes == 'exit':
#         break
# sock.close()
# s.close()
