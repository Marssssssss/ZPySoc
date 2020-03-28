# --coding=utf-8--
import Configure.conf


# 指令流处理模块
# 该模块负责将输入进行处理并进行相应的动作
# 处理层级: raw -> singleCommand -> [command, args] -> list([command, args])
# 注意: 在分解成 args 的时候空格并不会消失，而是会保留到字串内，因此后续处理需要注意
class MessageProcess(object):
    def __init__(self):
        pass

    # 将消息直接处理到最后一个等级, 并全部放到一个列表里面返回
    def split(self, raw):
        if raw == "":
            return None
        commands = self.splitInput(raw)
        result = []
        for command in commands:
            result.append(self.splitSingleCommand(command))
        return result

    # 将一条消息处理为多个单指令
    def splitInput(self, raw):
        commands = []  # every single command will be put into this list and ready to return
        msg = raw

        start = self.__strIndex(msg, "$")
        end = start
        if start != 0:
            return commands
        while end != -1:
            end = self.__strIndex(msg, "$", end + 1)
            if end == -1:
                commands.append(msg[start:])
                break
            if msg[end - 1] != "\\":
                commands.append(msg[start: end])
                start = end

        return commands

    # 单个指令的处理，将指令的具体指令和其所需要的参数分开，返回为 [command, args] 形式
    # singleCom: single command
    def splitSingleCommand(self, singleCom):
        # if length is 1, that means singleCom is $
        if len(singleCom) == 1:
            return None

        index = 1
        while index < len(singleCom):
            if singleCom[index] == "$" and singleCom[index - 1] == "\\":
                singleCom = singleCom[:index - 1] + singleCom[index:]
                index -= 1
            index += 1

        args = []  # ready for return
        start = 0
        end = self.__strIndex(singleCom, " ")
        if end == -1:
            command = singleCom[start:][1:]  # ready for return
            return [command, args]

        # get params
        command = singleCom[start:end][1:]  # ready for return
        start = end + 1
        while end != -1:
            end = self.__strIndex(singleCom, " ", start)
            if end == -1:
                args.append(singleCom[start:])
                break
            args.append(singleCom[start: end + 1])
            start = end + 1

        return [command, args]

    # 另一种形式的 string.index，找不到指定字串时跳过异常
    def __strIndex(self, str, target, begin=0):
        try:
            result = str.index(target, begin)
        except:
            result = -1

        return result
