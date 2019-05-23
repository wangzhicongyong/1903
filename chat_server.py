"""
服务端(udp)
"""
from socket import*
import os,sys
addr = ('0.0.0.0',9965)
#存储用户信息
user = {}
def do_login(s,name,addr):
    """
    登录聊天室
    :param s:
    :param name:
    :param addr:
    :return:
    """
    if name in user or "管理员" in name: # 如果名字里含有管理员三个字符
        s.sendto("\n该用户已存在".encode(),addr)
        return
    s.sendto(b'ok',addr)
    #通知其他人
    msg = '\n欢迎%s进入聊天室'% name
    for i in user:
        s.sendto(msg.encode(),user[i])
    #将用户存入
    user[name] = addr

#聊天
def do_chat(s,name,text):
        msg = '%s:%s'%(name,text)
        for i in user:
            if i != name:
                s.sendto(msg.encode(),user[i]) # user[i]是每个用户的地址

#退出
def do_quit(s,name):
    msg = '\n%s退出了聊天室'%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    #将用户删除

    del user[name]


#接收客户端各种请求
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        #区分类型 是为了弄清楚客户端发过来的请求是要干什么事
        if msg[0] =="L":
            do_login(s,msg[1],addr)   #msg[1]是name
        elif msg[0] =="C":
            text = " ".join(msg[2:])
            do_chat(s,msg[1],text)
        elif msg[0] == 'Q':
            if msg[1] not in user:
                s.sendto(msg[1],addr)
                continue
            do_quit(s,msg[1])



#创建网络连接
def main():
    s = socket(AF_INET,SOCK_DGRAM) #UDP协议
    s.bind(addr)
    pid = os.fork() #多进程一边处理请求/一边发送消息
    if pid < 0:
        return
    #发送管理员消息
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = 'C 管理员消息 '+ msg
            s.sendto(msg.encode(),addr)
    else:
        #请求处理
        do_request(s) #处理客户端请求


if __name__ == "__main__":
    main()