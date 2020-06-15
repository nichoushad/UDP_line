#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  在此，我感谢 渣渣灰对我的启发和帮助。下面的报告中，我还会具体地提到
#  他们在各个方法对我的帮助。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。

#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
#  林峰

from socket import *
import sys
from threading import *
from udp_lines.login import *


def login_to_line(sock, users, username, password, addr):
    if login(username, password):
        sock.sendto(b'OK', addr)
        msg = '\n%s 进入聊天室' % username
        for i in users:
            sock.sendto(msg.encode(), users[i])
        # 将用户插入字典
        users[username] = addr
        print(users)
    else:
        sock.sendto(b'username or password error!', addr)


def register_to_line(sock, username, password, addr):
    if register(username, password):
        sock.sendto(b'register success!', addr)
    else:
        sock.sendto(b'it has been registered!', addr)


def chat_to_all(sock, users, username, text):
    msg = '\n%-4s 说:%s' % (username, text)
    # 发给所有人,除了自己
    for i in users:
        if i != username:
            sock.sendto(msg.encode(), users[i])


def chat_to_one(sock, users, username, to_username, text):
    msg = '\n%-4s私聊你说:%s' % (username, text)
    # 私聊
    if username == to_username:
        sock.sendto(b'\ndo not send message to yourself', users[username])
    elif to_username in users:
        sock.sendto(msg.encode(), users[to_username])
    else:
        sock.sendto(b'\nno this people', users[username])


def quit(sock, users, username):
    print(username + ' leave')
    del users[username]
    msg = '\n' + username + '离开了聊天室'
    for i in users:
        sock.sendto(msg.encode(), users[i])


def update_to_line(sock, username, password, addr):
    if update(username, password):
        str = '\n'+username+ 'password update success!'
        sock.sendto(str.encode(), addr)
    else:
        str = '\n' + username + 'password update fail!'
        sock.sendto(str.encode(), addr)


# 接收客户端请求并处理
def run(sock):
    users = {}
    while True:
        msg, addr = sock.recvfrom(1024)
        msgList = msg.decode().split(' ')
        # 判断请求类型进行处理
        if msgList[0] == 'R':
            register_to_line(sock, msgList[1], msgList[2], addr)
        if msgList[0] == 'L':
            login_to_line(sock, users, msgList[1], msgList[2], addr)
        elif msgList[0] == 'C':
            chat_to_all(sock, users, msgList[1], ' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            quit(sock, users, msgList[1])
        elif msgList[0] == 'P':
            chat_to_one(sock, users, msgList[1], msgList[2], ' '.join(msgList[3:]))
        elif msgList[0] == 'U':
            update_to_line(sock, msgList[1], ' '.join(msgList[2:]),addr)


if __name__ == '__main__':
    ADDR = ('127.0.0.1', 1060)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)
    run(sock)

