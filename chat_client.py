"""
客户端
"""
from socket import*
import os,sys
#服务器地址
server_addr = ('127.0.0.1',9965)
#创建网络连接
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名")
        msg = 'L ' + name #一种协议
        sockfd.sendto(msg.encode(),server_addr)
        #等待回应
        data,addr = sockfd.recvfrom(1024)
        if data.decode() == 'ok':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    # 创建duo进程(目的是达到收发消息同时操作)
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(sockfd, name)
    else:
        recv_msg(sockfd)

#发消息
def send_msg(s,name):
    while True:
        try:
            text = input('发言:')
        except:
            text ='quit'
        #退出聊天室
        if text == 'quit':
            msg = 'Q '+name
            s.sendto(msg.encode(),server_addr)
            sys.exit("退出聊天室")
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),server_addr)

#收消息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        #服务端发送exit表示让客户端退出
        if data.decode() == 'EXIT':
            sys.exit()
        print(data.decode())




if __name__ =="__main__":
    main()