# --coding=utf-8--

import Message.messageProcess as messageProcess
import Configure.conf as conf
import netStream
import netListener
import time
import threading


# 简单主机类
# 该类实现简单的服务器
class simpleHost(object):
    def __init__(self, maxClients):
        self.maxClients = maxClients

        self.listener = netListener.NetListener("0.0.0.0", 8888, self.maxClients)
        self.msgProc = messageProcess.MessageProcess()  # message process
        self.streamSlots = [netStream.NetStream(x) for x in range(self.maxClients)]  # netStream slots

        self.netState = conf.NET_STATE_STOP
        self.netThread = None
        self.messageBox = []
        self.rawRecvBuffer = []  # format: list([sid, msg])
        self.sendBuffer = []  # format: list([source, msg, target])

        self.tick = 1 / 60  # server refresh tick

    # 主机服务器开始运作
    def start(self):
        self.listener.startListen()

        self.netThread = threading.Thread(target=self.__netThread, args=[])
        self.netThread.setDaemon(True)
        self.netThread.start()

        while self.netState == conf.NET_STATE_ESTABLISHED:
            pass

    # 关闭该主机服务器
    def close(self):
        for stream in self.streamSlots:
            stream.close()
        self.listener.close()

        self.netState = conf.NET_STATE_CLOSING

    # 添加需要发送的消息
    def addMsgToSendBuffer(self, source, msg, target):
        self.sendBuffer.append([source, msg, target])

    # 网络进程的执行过程
    def __netThread(self):
        self.netState = conf.NET_STATE_ESTABLISHED
        while self.netState == conf.NET_STATE_ESTABLISHED:
            self.__process()
        self.netState = conf.NET_STATE_STOP

    # 每 tick 执行流程
    def __process(self):
        if self.netState != conf.NET_STATE_ESTABLISHED:
            return

        # main process
        startTime = time.time()

        self.__acceptClients()
        self.__sendMessages()
        self.__recvMessages()

        sleepTime = self.tick - (time.time() - startTime)
        if sleepTime < 0:
            sleepTime = 0
        time.sleep(sleepTime)

    # 将所有待发送消息发送出去
    def __sendMessages(self):
        size = len(self.sendBuffer)
        for send in self.sendBuffer[:size]:
            source = send[0]
            msg = send[1]
            target = send[2]
            self.streamSlots[target].sendData(msg)
        self.sendBuffer = self.sendBuffer[size:]

    # 从所有的网络流中接收消息 [sid, msg]
    def __recvMessages(self):
        sid = 0
        for sid in range(len(self.streamSlots)):
            msg = self.streamSlots[sid].getRecvData()
            if msg != "":
                self.rawRecvBuffer.append([sid, msg])

    # 接收等待连入的所有连接
    def __acceptClients(self):
        connAddrList = self.listener.getAllConn()
        if len(connAddrList) == 0:
            return 0

        successCount = 0
        for connAddr in connAddrList:
            if self.__putIntoEmptyNetStreamSlot(connAddr):
                successCount += 1
            else:
                connAddr[0].sendall("[Server] Sorry, server is full!")

        return successCount

    # 将连接放入空的网络流插槽中
    def __putIntoEmptyNetStreamSlot(self, connAddr):
        index = 0
        while not self.streamSlots[index].assign(connAddr[0], connAddr[1]):
            index += 1
            if index == self.maxClients:
                return False
        self.streamSlots[index].start()
        return True

