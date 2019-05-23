"""1.搭建网络2.查看文件库信息"""
from socket import*
from threading import Thread
import os,sys
from time import sleep
#粘包的解决方案：延迟(sleep)/人为添加消息边界


#搭建网络 全局变量
host = '0.0.0.0'
port = 8888
Addr = (host,port)
Ftb = "/home/tarena/ftb/" #文件库路径

#1.写功能的时候首先要定全局变量(一般是很多函数要用的＼其次是有特殊含义的)

#将客户端请求功能封装为类
class FtbServer:
    def __init__(self,connfd,Ftb_path):
        self.connfd = connfd
        self.path = Ftb_path

    def do_list(self):
        """获取文件列表"""
        files = os.listdir(self.path)#查看文件列表
        if not files:
            self.connfd.send("该文件类型为空".encode())
            return
        else:
            self.connfd.send(b'ok')
            sleep(0.1)
        # 相当于把他们组合成一个大字符串
        fs =" "
        for file in files:
            #判断文件类型是否是隐藏文件和普通文件..
            if file[0] !='.' and \
                os.path.isfile(self.path+file):#查看文件类型
                #sleep(0.1)
                fs += file + '\n'
        self.connfd.send(fs.encode())

    def do_get(self,filename):
        try:
            fd = open(self.path+filename,'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'ok')
            sleep(0.1)
        #发送文件内容
        while True:
            data = fd.read(1024)
            #文件结束
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
    def do_put(self,filename):
        if os.path.exists(self.path+filename): #查看文件是否存在
            self.connfd.send("该文件已存在".encode())
            return
        self.connfd.send(b'ok')
        fd = open(self.path+filename,'wb')
        #接收文件
        while True:
            data = self.connfd.recv(1024)
            if data ==b'##':
                break
            fd.write(data)
        fd.close()


def handle(connfd):
    """
    客户端请求处理函数
    :param connfd: 客户端链接
    :return:
    """
    #选择文件夹
    cls = connfd.recv(1024).decode()
    Ftb_path = Ftb +cls + '/'
    ftb = FtbServer(connfd, Ftb_path) #ftb 对象
    while True:
        #接收客户端信息
        data = connfd.recv(1024).decode()
        #如果客户端断开返回data为空,服务端可以及时作出选择
        if not data or data[0] == 'q':
            return
        elif data[0] =='l':
            ftb.do_list()
        elif data[0] =='g':
            filename = data.split(" ")[-1]
            ftb.do_get(filename)
        elif data[0] =='p':
            filename = data.split(" ")[-1]
            ftb.do_put(filename)




def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(Addr)
    s.listen(5)
    print("wait for client.....")
    while True:
        try:
            c,addr = s.accept()
        except KeyboardInterrupt:
            sys.exit("fu wu qi tui chu")
        except Exception as e:
            print(e)
            continue
        print('链接的客户端',addr)

        client = Thread(target=handle,args=(c,))
        client.setDaemon(True)
        client.start()
if __name__ =="__main__":
        main()


