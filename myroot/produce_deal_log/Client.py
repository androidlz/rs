# coding: utf - 8
import socket
import os

host = socket.gethostname()
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect((host, 8888))
# f=oprn('aa','wb')
# ss.sendall('g7d245PQR3&six&Windows Gecko Firefox&192.168.1.100&7103954&topic_hahaha&0&5'.encode())  # 发送小明的用户id
# ss.sendall('9527&&1'.encode())  # 发送小明的用户id=9527   点击行为 1
ss.sendall('12&&1'.encode())  # 用户点击了电影条目id为1    服务端返回相关电影推荐
# os.system('sleep 1')
ss.send('EOF'.encode())
data = ss.recv(1024)
print('server back %s' % data.decode())
ss.close()




# import socket
#
# s = socket.socket()
# host = socket.gethostname()
# port = 12347
# s.connect((host, port))
# print('Linked')
# info = ''
# while True:
#     send_mes = input("input your message\r\n")
#     s.send(send_mes.encode())
#     if send_mes == 'exit':
#         break
#     info = s.recv(1024).decode()
#     print('receive:' + info)
# s.close()
