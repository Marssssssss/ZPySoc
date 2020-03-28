# --coding=utf-8--

import Network.simpleHost as simpleHost
import Message.events as events
import Configure.conf as conf
import Configure.help as help


# 服务器模块
# 该服务器的内容可以进行自定义，用事件类来定义指令的回调函数并绑定即可
class Server(object):
    def __init__(self, maxClients):
        self.host = simpleHost.SimpleHost(maxClients)
        self.registerInfo = {}
        self.clientInfo = []
        self.serverCommand = []
        self.__registerEvents()

    def start(self):
        self.host.start()
        while self.host.netState == conf.NET_STATE_ESTABLISHED:
            self.serverCommand = raw_input()
            self.__commandDeal()

    def close(self):
        self.host.close()

    def __commandDeal(self):
        # todo
        pass

    def __registerEvents(self):
        self.host.evHandler.addEvent("help", msgEventHelp())
        self.host.evHandler.addEvent("chat", msgEventChat())
        self.host.evHandler.addEvent("create", msgEventCreate(self))


# 事件类
# 定义命令的行为
# $help
class msgEventHelp(events.MsgEvent):
    def __init__(self):
        super(msgEventHelp, self).__init__("help", self.__msgEventHelpCallback)

    def __msgEventHelpCallback(self, args):
        # pre-process args, clear space on both side
        for i in range(len(args)):
            args[i] = args[i].strip()

        # begin process
        if len(args) == 0:
            return [[help.NET_HELP_TIPS_ALL, self.sid]]
        else:
            unknownCommand = []
            result = help.NET_HELP_TIPS_HEAD
            for arg in args:
                if arg in help.tipsForSingleCommand.keys():
                    result += "  " + help.tipsForSingleCommand[arg] + "\n"
                else:
                    unknownCommand.append(arg)
            if len(unknownCommand) == 0:
                return [[result, self.sid]]

            result += help.NET_HELP_TIPS_UNKNOWN_HEAD
            result += unknownCommand[0]
            unknownCommand = unknownCommand[1:]
            for command in unknownCommand:
                result += ", " + command
            return [[result, self.sid]]


# $chat
class msgEventChat(events.MsgEvent):
    def __init__(self):
        super(msgEventChat, self).__init__("chat", self.__msgEventChatCallback)

    def __msgEventChatCallback(self, args):
        message = ""
        for arg in args:
            message += arg
        if message == "":
            return []
        # -1 means broadcast
        return [[message + " ", -1]]


# $create
class msgEventCreate(events.MsgEvent):
    def __init__(self, father):
        super(msgEventCreate, self).__init__("create", self.__msgEventChatCallback)
        self.father = father

    def __msgEventChatCallback(self, args):
        # too many args
        if len(args) > 2:
            return [[conf.NET_COMMAND_CREATE_TOO_MANY_ARGS, self.sid]]

        username = args[0]
        password = args[1]

        # username has existed
        if username in self.father.registerInfo.keys():
            return [[conf.NET_COMMAND_CREATE_USERNAME_EXISTED, self.sid]]

        # success
        self.father.registerInfo[username] = password
        print self.father.registerInfo
        return [[conf.NET_COMMAND_CREATE_SUCCESS, self.sid]]


