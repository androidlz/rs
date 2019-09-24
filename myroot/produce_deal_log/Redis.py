# 一致性哈希适应
'''
terminal用的命令：
>cd d:\program\redis
>redis-server --port 6380
>redis-cli
>KEYS *
'''

import redis as redis
from hash_ring import *
from hash_ring.hash_ring import HashRing

# 实例化两个服务器
memcache_servers = ['127.0.0.1:6379', '127.0.0.1:6380']
# HashRing初始化hash环的机器列表
ring = HashRing(memcache_servers)
# 存储数据  找到数据对应的数据单元的server，连接server 再把数据写进去
server = ring.get_node('my_key2232')
print(server)
# 普通连接
conn = redis.Redis(server.split(':')[0], int(server.split(':')[1]), 0)
conn.set("my_key2232", "123123123")  # 写
# val = conn.get("x1")
# print(val)


# server = ring.get_node('my_key')
# print(server)
# # 普通连接
# conn = redis.Redis(server.split(':')[0], int(server.split(':')[1]), 0)
# conn.set("my_key", "123123123")
#
# server = ring.get_node('my_key')
# r = redis.Redis(server.split(':')[0], int(server.split(':')[1]), 0)
# print(server)
# print(r.get('my_key'))  # 读
