# --coding=utf-8--


# 事件类
# 该类是所有事件类的父类
class msgEvent(object):
    def __init__(self, name, cb):
        self.eventName = name
        self.callBack = cb
        self.sendMsg = ""
        self.sourceID = -1  # 该事件的来源，即接收命令的网络流的 sid

    def trigger(self, args):
        self.callBack(args)


# chat command
class msgEventChat(msgEvent):
    def __init__(self, name, cb) :
        super(msgEventChat, self).__init__(name, cb)
