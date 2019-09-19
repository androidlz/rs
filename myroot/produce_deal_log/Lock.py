# 多线程内存更新
import threading
from time import sleep, ctime


class Lock:
    # 全局锁  0 表示可以读  1表示可以写
    lock = 0
    cate_items = {}
    file = open('./thefile.txt')

    def __init__(self):
        for line in self.file.readlines():
            line = line.strip()
            ls = line.split('&')
            if ls[5] not in self.cate_items.keys():
                self.cate_items[ls[5]] = []
            self.cate_items[ls[5]].append(ls[4])

    def write(self):
        print("writing.....")
        while True:
            if self.lock == 0:
                self.lock = 1
                for line in self.file.readlines():
                    line = line.strip()
                    ls = line.split('&')
                    if ls[5] not in self.cate_items.keys():
                        self.cate_items[ls[5]] = []
                    self.cate_items[ls[5]].append(ls[4])
                self.lock = 0
                print('write successed')
            else:
                print('write failed sleep')
            sleep(1)

    # 读写分离   读的时候不写  写的时候不读
    def read(self):
        print("reading.....")
        while True:
            if self.lock == 0:
                for k, v in self.cate_items.items():
                    line = k + '\t' + '&&'.join(v) + "\n"
                    # print(line)
                    break
                print('read successed')
            else:
                print('read failed sleep')
            sleep(1)


if __name__ == "__main__":
    l = Lock()
    threads = []
    t1 = threading.Thread(target=l.read)
    threads.append(t1)
    t2 = threading.Thread(target=l.write)
    threads.append(t2)

    for t in threads:
        # 后台执行一次  就不再执行
        # t.setDaemon(True)
        t.start()
