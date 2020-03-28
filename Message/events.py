# --coding=utf-8--


# 事件类
# 该类是所有事件类的父类
# 回调函数需要返回 list([msg, target]), 如果参数错误等错误的情况需要返回 None
class MsgEvent(object):
    def __init__(self, name, cb):
        self.eventName = name
        self.callback = cb
        self.sid = -1  # 该事件的来源，即接收命令的网络流的 sid

    # 触发该事件的回调函数
    def trigger(self, args, sid):
        self.sid = sid
        return self.callback(args)

    # 设置事件的回调函数
    def setCallBackFunc(self, func):
        self.callback = func





