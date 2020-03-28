# --coding=utf-8--
import socket
import threading
import Configure.conf as conf
import time


# 服务器网络数据传输流模块 ==ServerOnly
# 该模块负责单连接数据的接收和发送，并将接收和发送的数据暴露给其他使用该模块的模块
class NetStream(object):
    def __init__(self, id):
        self.sock = None
        self.addr = None
        self.sendBuf = ""
        self.recvBuf = ""

        self.recvThread = None
        self.sendThread = None

        self.sid = id  # stream id
        self.netState = conf.NET_STATE_STOP
        self.netType = conf.NET_TYPE_UNKNOWN
        self.info = {}

    # 连接到指定主机
    def connect(self, host, port):
        if self.netState != conf.NET_STATE_STOP:
            return
        self.addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setblocking(0)
        self.netState = conf.NET_STATE_ESTABLISHED
        self.sendBuf = ""
        self.recvBuf = ""
        self.netType = conf.NET_TYPE_CS

    # 给该实例分配 socket 连接和地址
    def assign(self, conn, addr):
        if self.netState != conf.NET_STATE_STOP:
            return False
        self.addr = addr
        self.sock = conn
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setblocking(0)
        self.netState = conf.NET_STATE_ESTABLISHED
        self.sendBuf = ""
        self.recvBuf = ""
        self.netType = conf.NET_TYPE_SC
        return True

    # 设置该实例的 sid
    def setSID(self, id):
        self.sid = id

    # 获取该实例的 sid
    def getSID(self):
        return self.sid

    # 开始消息收发
    def start(self):
        if self.netState != conf.NET_STATE_ESTABLISHED:
            return

        if self.recvThread is None or not self.recvThread.isAlive():
            self.recvThread = threading.Thread(target=self.__recvBufThread, args=[])
            self.recvThread.setDaemon(True)
            self.recvThread.start()

        if self.sendThread is None or not self.sendThread.isAlive():
            self.sendThread = threading.Thread(target=self.__sendBufThread, args=[])
            self.sendThread.setDaemon(True)
            self.sendThread.start()

    # 关闭连接
    def close(self):
        if self.netState != conf.NET_STATE_ESTABLISHED:
            return

        self.netState = conf.NET_STATE_CLOSING
        while self.sendThread.isAlive() or self.recvThread.isAlive():
            pass
        self.sock.close()
        self.netState = conf.NET_STATE_STOP

    # 消息发送用线程
    def __sendBufThread(self):
        while self.netState == conf.NET_STATE_ESTABLISHED:
            if self.sendBuf != "" and self.netState == conf.NET_STATE_ESTABLISHED:
                self.sock.sendall(self.sendBuf)
                self.sendBuf = ""

    # 消息接收用线程
    def __recvBufThread(self):
        tempBuf = ""
        while self.netState == conf.NET_STATE_ESTABLISHED:
            self.recvBuf += tempBuf
            tempBuf = ""
            try:
                tempBuf = self.sock.recv(4096)
            except:
                pass

    # 获取接收到的数据
    def getRecvData(self):
        size = len(self.recvBuf)
        td = self.recvBuf[0:size]
        self.recvBuf = self.recvBuf[size:]
        return td

    # 添加要发送的数据
    def sendData(self, new):
        self.sendBuf += new

