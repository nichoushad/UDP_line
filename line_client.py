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
import threading


# 发送消息
def send_msg(sock, username, ADDR):
    while True:
        text = input('发言(quit退出，C全体，P+to_username私聊，U+new_password更新密码):')
        msgList = text.split(' ')
        if text.strip() == 'quit':
            msg = 'Q ' + username
            sock.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')
        # 聊天
        elif msgList[0] == 'C':
            msg = 'C %s %s' % (username, ' '.join(msgList[1:]))
            sock.sendto(msg.encode(), ADDR)
        elif msgList[0] == 'P':
            msg = 'P %s %s %s' % (username, msgList[1], ' '.join(msgList[2:]))
            sock.sendto(msg.encode(), ADDR)
        elif msgList[0] == 'U':
            msg = 'U %s %s' % (username,  ' '.join(msgList[1:]))
            sock.sendto(msg.encode(), ADDR)


def rcv_msg(sock):
    while True:
        msg, addr = sock.recvfrom(1024)
        print(msg.decode()+'\n发言(quit退出，C全体，P+to_username私聊，U+new_password更新密码):', end='')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 1060
    ADDR = (HOST, PORT)
    sock = socket(AF_INET, SOCK_DGRAM)

    # 登录
    while True:
        msg = input('登录：L + name + password\n注册：R + name + password\n')
        sock.sendto(msg.encode(), ADDR)
        msgList = msg.split(' ')
        if msgList[0] == 'R':
            data, addr = sock.recvfrom(1024)
            print(data.decode())
            continue
        else:
            data, addr = sock.recvfrom(1024)
            if data.decode() == 'OK':
                print('进入聊天室')
                break
            else:
                # 输出错误
                print(data.decode())
                continue
    # 渣渣辉教我的多线程
    t1 = threading.Thread(target=send_msg, args=(sock, msgList[1], ADDR,))
    t2 = threading.Thread(target=rcv_msg, args=(sock,))
    t1.start()
    t2.start()
