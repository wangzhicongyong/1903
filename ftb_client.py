import time
import sys
from socket import*
#具体功能
class FtbClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        """
        获取文件列表
        :return:
        """
        self.sockfd.send(b'l')#发送请求
        #等待回复
        data = self.sockfd.recv(128).decode()
        #ok表示请求成功
        if data == 'ok': #false
            #接收文件列表
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)
    def do_quit(self):
        self.sockfd.send(b'q')
        self.sockfd.close()
        sys.exit("谢谢使用")
    def do_get(self,filename):
        """
        下载文件
        :param filename:
        :return:
        """
        #发送请求
        self.sockfd.send(('g'+filename).encode())
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data =='ok':
            fd = open(filename,'wb')
            #接收内容写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                fd.write(data)
            fd.close()
        else:
            print(data)

    def do_put(self,filename):
        """
        上传文件
        :param filename:
        :return:
        """
        try:
            f = open(filename,'rb')
        except Exception:
            print('没有该文件')
            return

        # 发送请求
        filename = filename.split('/')[-1]
        self.sockfd.send(('p' + filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'ok':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print(data)

#发起请求
def request(sockfd):
    ftb = FtbClient(sockfd)
    while True:
        print('\n........命令选项.........')
        print('..........list............')
        print('........get file..........')
        print('........put file..........')
        print('........quit..............')

        cmd = input('输入命令：')
        if cmd.strip() == 'list':
            ftb.do_list()#函数参数由功能来定
        elif cmd.strip() == 'quit':
            ftb.do_quit()
        elif cmd[:3] == 'get':
            filename = cmd.strip().split(" ")[-1]
            ftb.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(" ")[-1]
            ftb.do_put(filename)


#网络链接
def main():
    #服务器地址
    addr = ('127.0.0.1',8888)
    sockfd = socket()
    try:
        sockfd.connect(addr)
    #有异常则执行
    except Exception as e:
        print("链接服务器失败")
        return
    else:
        print("""
               data file img""")
        cls = input("请选择文件类别:")
        if cls not in ['data','file','img']:
            print('nin shu ru cuo wu')
            return
        else:
            sockfd.send(cls.encode())
            # 发送具体请求
            request(sockfd)

if __name__ == "__main__":
    main()

