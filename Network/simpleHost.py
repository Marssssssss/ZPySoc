# --coding=utf-8--

import Message.messageProcess as messageProcess
import Message.eventHandler as eventHandler
import Configure.conf as conf
import netStream
import netListener
import time
import threading


# 简单主机类
# 该类实现简单的主机，外部可以根据需求自定义该主机的功能
# evHandler.callBackList[command] = eventObject(name, cb) 可以定义自己的事件
# evHandler.callBackList[command].setCallbackFunc(func) 可以自定义该事件的回调函数，其返回值必须为列表，列表内是将要送回的信息
#                                                       目标对 [msg, target]
class SimpleHost(object):
    def __init__(self, maxClients):
        self.maxClients = maxClients

        self.__listener = netListener.NetListener("0.0.0.0", 8888, self.maxClients)  # net listener
        self.__msgProc = messageProcess.MessageProcess()  # message process
        self.__streamSlots = [netStream.NetStream(x) for x in range(self.maxClients)]  # netStream slots
        self.evHandler = eventHandler.EventHandler()  # event handler

        self.netState = conf.NET_STATE_STOP
        self.netThread = None
        self.rawRecvBuffer = [[x, ""] for x in range(self.maxClients)]  # format: list([sid, msg])
        self.sendBuffer = []  # format: list([source, msg, target])

        self.userPermission = [0 for x in range(self.maxClients)]  # init user permission

        self.tick = 1 / 60  # server refresh tick

    # 主机服务器开始运作
    def start(self):
        self.__listener.startListen()

        self.netThread = threading.Thread(target=self.__netThread, args=[])
        self.netThread.setDaemon(True)
        self.netState = conf.NET_STATE_ESTABLISHED
        self.netThread.start()

    # 关闭该主机服务器
    def close(self):
        for stream in self.__streamSlots:
            stream.close()
        self.__listener.close()

        self.netState = conf.NET_STATE_CLOSING

    # 赋予某一权限
    def invokePermission(self, sid, permit):
        self.userPermission[sid] |= permit

    # 关闭某一权限
    def cancelPermission(self, sid, permit):
        self.userPermission[sid] &= ~permit

    # 检查是否有某一权限
    def checkPermission(self, sid, command):
        return self.userPermission[sid] & conf.permissionList[command] != 0

    # 添加需要发送的消息, target = -1 表示广播
    def addMsgToSendBuffer(self, source, msg, target):
        if target == -1:
            for index in range(self.maxClients):
                self.sendBuffer.append([source, msg, index])
        else:
            self.sendBuffer.append([source, msg, target])

    # 网络进程的执行过程
    def __netThread(self):
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
        self.__dealMessages()

        sleepTime = self.tick - (time.time() - startTime)
        if sleepTime < 0:
            sleepTime = 0
        time.sleep(sleepTime)

    # 将所有待发送消息发送出去
    def __sendMessages(self):
        size = len(self.sendBuffer)
        for send in self.sendBuffer[:size]:
            msg = send[1]
            target = send[2]
            self.__streamSlots[target].sendData(msg)
        self.sendBuffer = self.sendBuffer[size:]

    # 从所有的网络流中接收消息 [sid, msg]
    def __recvMessages(self):
        sid = 0
        for sid in range(len(self.__streamSlots)):
            msg = self.__streamSlots[sid].getRecvData()
            if msg != "":
                self.rawRecvBuffer[sid][1] += msg

    # 将所有的 rawRecvMessage 进一步处理为 sendMessage 要求的格式
    # 可以根据需求进一步扩展
    def __dealMessages(self):
        sid = 0
        while sid < self.maxClients:
            size = len(self.rawRecvBuffer[sid][1])
            msg = self.rawRecvBuffer[sid][1][:size]
            self.rawRecvBuffer[sid][1] = self.rawRecvBuffer[sid][1][size:]

            midMsgs = self.__msgProc.split(msg)  # midMsgs = list([command, args]), midMsg = [command, args]
            if midMsgs is not None:
                for midMsg in midMsgs:
                    # check command permission
                    if midMsg[0] in conf.permissionList.keys() and not self.checkPermission(sid, midMsg[0]):
                        self.addMsgToSendBuffer(-1, "[Server]Sorry! You have no permission to use this command!", sid)
                        continue

                    # trigger event
                    response = self.evHandler.triggerEvent(midMsg, sid)  # triggerEvent([command, args], sid)
                    if response is None:
                        self.addMsgToSendBuffer(-1, "[Server]Command error! Please check your command or arguments!"
                                                    " Input $help for help!", sid)
                    else:
                        for result in response:
                            self.addMsgToSendBuffer(sid, result[0], result[1])
            sid += 1

    # 接收等待连入的所有连接
    def __acceptClients(self):
        connAddrList = self.__listener.getAllConn()
        if len(connAddrList) == 0:
            return 0

        successCount = 0
        for connAddr in connAddrList:
            if self.__putIntoEmptyNetStreamSlot(connAddr):
                successCount += 1
            else:
                connAddr[0].sendall("[Server]Sorry, server is full!")

        return successCount

    # 将连接放入空的网络流插槽中
    def __putIntoEmptyNetStreamSlot(self, connAddr):
        index = 0
        while not self.__streamSlots[index].assign(connAddr[0], connAddr[1]):
            index += 1
            if index == self.maxClients:
                return False
        self.userPermission[index] = conf.NET_PERMISSION_LOGIN | conf.NET_PERMISSION_CREATE
        self.__streamSlots[index].start()
        return True

