#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  在此，我感谢 XXX, …, XXX对我的启发和帮助。下面的报告中，我还会具体地提到
#  他们在各个方法对我的帮助。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。

#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
#  林峰

import pymysql
import hashlib


def register(username, password):
    db = pymysql.connect(host="localhost", user="root",
                         password="waz123", port=3306)
    cursor = db.cursor()
    md5 = hashlib.md5()
    # 加密加盐，使其难以破解
    md5.update((password + 'lf' + username).encode("utf-8"))
    # 拿到加密字符串
    md = md5.hexdigest()
    # 生成哈希值，加密后的password存进数据库
    real_password = md
    # insert进数据库
    sql = "INSERT INTO user_system.LOGIN(USERNAME, PASSWORD) VALUES('{username}', '{password}')" \
        .format(username=username, password=real_password)
    try:
        # 提交表单到mysql
        cursor.execute(sql)
        db.commit()
        db.close()
        print(username + ' register success!')
        return True
    except:
        db.rollback()
        print(username +' register fail!')
        return False


def login(username, password):
    db = pymysql.connect(host="localhost", user="root",
                         password="waz123", port=3306)
    cursor = db.cursor()
    md5 = hashlib.md5()
    md5.update((password + 'lf' + username).encode("utf-8"))
    md = md5.hexdigest()
    real_password = md
    sql = "SELECT PASSWORD FROM user_system.LOGIN WHERE USERNAME = '%s'" % (username)
    cursor.execute(sql)
    # username是主键，至多有一条纪录

    pwd1 = cursor.fetchone()
    if (pwd1 == None):
        print(username + 'username or password error!')
        return False
    pwd = pwd1[0]
    # 返回状态
    if pwd == real_password:
        print(username + ' login success!')
        return True
    else:
        print(username +' username or password error!')
        return False


# 更新密码
def update(username, password):
    db = pymysql.connect(host="localhost", user="root",
                         password="waz123", port=3306)
    cursor = db.cursor()
    md5 = hashlib.md5()
    md5.update((password + 'lf' + username).encode("utf-8"))
    md = md5.hexdigest()
    real_password = md
    sql = "UPDATE user_system.LOGIN SET PASSWORD = '%s' WHERE USERNAME = '%s'" % (real_password, username)
    try:
        cursor.execute(sql)
        db.commit()
        print(username + ' password update success!')
        return True
    except:
        db.rollback()
        print(username + ' password update fail!')
        return False
