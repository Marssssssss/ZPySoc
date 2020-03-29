# --coding=utf-8--
import events


# 事件管理器模块
# 该模块负责管理事件，接收消息然后触发相应事件并获取返回值
class EventHandler(object):
    def __init__(self):
        self.eventDict = {}

    # 根据消息触发相应事件,消息格式为 [command, args]
    def triggerEvent(self, msg, sid):
        if msg[0] in self.eventDict.keys():
            return self.eventDict[msg[0]].trigger(msg[1], sid)
        return None

    def addEvent(self, name, msgEvent):
        if name in self.eventDict.keys():
            raise EventExistedError("Event has existed! Event name: " + name)
        self.eventDict[name] = msgEvent


# '事件已存在'异常
class EventExistedError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value