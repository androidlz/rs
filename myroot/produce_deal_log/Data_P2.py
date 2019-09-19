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

# 6379在写   6380在读    读完之后反馈到服务端
r = redis.Redis('127.0.0.1', 6379, db=0)
r2 = redis.Redis('127.0.0.1', 6380, db=0)
while True:
    m = r.get('9527#1')
    m2 = r2.get('9527#1')
    r2.set('9527#1', m)  # 写
    print(r.get('9527#1'))
