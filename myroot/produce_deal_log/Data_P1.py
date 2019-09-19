# 一致性哈希适应
'''
terminal用的命令：
>cd d:\program\redis
>redis-server --port 6380
>redis-cli
>KEYS *
'''

#  第一级redis是6379   第二级6380
import redis as redis
from hash_ring import *
from hash_ring.hash_ring import HashRing

# 普通连接
r = redis.Redis('127.0.0.1', 6379, db=0)
while True:
    m = r.get('9527#1')
    if m is None:
        r.set('9527#1', 1)  # 写
        print('set succeed')
    m = int(m) + 1
    r.set('9527#1', m)
    print(r.get('9527#1'))
