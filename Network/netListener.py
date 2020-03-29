# --coding=utf-8--
import socket
import threading
import Configure.conf as conf


# 网络监听模块
# 该模块负责监听外部连接，并将这些外部连接暴露给其他使用到该模块的模块
class NetListener(object):
    def __init__(self, host, port, num):
        self.socketListener = None
        self.hostData = None
        self.maxConnNum = 0
        self.connList = []
        self.addrList = []
        self.listenThread = None
        self.listenerState = conf.NET_STATE_STOP

        self.hostData = (host, port)
        self.maxConnNum = num

        self.needClear = False
        self.clearNum = 0

    # 更改 host 信息
    def changeHost(self, host=None, port=None, num=None):
        if self.listenerState != conf.NET_STATE_STOP:
            return

        if host is None:
            host = self.hostData[0]
        if port is None:
            port = self.hostData[1]
        self.hostData = (host, port)

        if num is not None:
            self.maxConnNum = num

    # 设置监听状态并开启监听
    def startListen(self):
        if self.listenerState != conf.NET_STATE_STOP:
            return
        self.socketListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketListener.bind(self.hostData)
        self.socketListener.listen(self.maxConnNum)

        # 单开一个线程进行端口监听
        self.listenThread = threading.Thread(target=self.__listenThreadFunc, args=())
        self.listenThread.setDaemon(True)
        self.listenThread.start()

    # 负责监听的线程
    def __listenThreadFunc(self):
        self.listenerState = conf.NET_STATE_ESTABLISHED

        while self.listenerState == conf.NET_STATE_ESTABLISHED:
            conn, addr = self.socketListener.accept()
            if self.needClear:
                self.connList = []
                self.addrList = []
                self.needClear = False
                self.clearNum = 0
            self.connList.append(conn)
            self.addrList.append(addr)

        # 停止监听器的运作
        self.socketListener.close()
        self.socketListener = None
        self.listenerState = conf.NET_STATE_STOP

    # 外部从该监听器内取出已经获取的连接
    def getAllConn(self):
        if self.needClear or self.listenerState != conf.NET_STATE_ESTABLISHED:
            return []
        size = len(self.connList)
        outputConn = self.connList[:size]
        outputAddr = self.addrList[:size]

        # pair one conn with one addr to a list
        outputPair = [[outputConn[x], outputAddr[x]] for x in range(size)]

        self.needClear = True
        self.clearNum = size
        return outputPair

    # 关闭监听器
    def close(self):
        if self.listenerState == conf.NET_STATE_ESTABLISHED:
            self.listenerState = conf.NET_STATE_CLOSING
