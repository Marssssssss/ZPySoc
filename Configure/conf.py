# --coding=utf-8--

# 网络状态
NET_STATE_STOP = 0
NET_STATE_CLOSING = 1
NET_STATE_CONNECTING = 2
NET_STATE_ESTABLISHED = 3

# 网络类型，用于 netStream
NET_TYPE_UNKNOWN = 0
NET_TYPE_SC = 1
NET_TYPE_CS = 2

# 命令
# command method: $command params
# if '$' is in params string ,it should follow after \
# To last commit: if a command end with \, it should end with space
NET_COMMAND_CREATE = "create"
NET_COMMAND_CREATE_TOO_MANY_ARGS = "[Server]Too many command arguments!\n"
NET_COMMAND_CREATE_USERNAME_EXISTED = "[Server]Username has existed, please try again!\n"
NET_COMMAND_CREATE_SUCCESS = "[Server]Username create/register success!\n"

NET_COMMAND_LOGIN = "login"

NET_COMMAND_LOGOUT = "logout"

NET_COMMAND_CHAT = "chat"

NET_COMMAND_INFO = "info"

NET_COMMAND_ROLL = "roll"

NET_COMMAND_ROLLSTART = "rollstart"

NET_COMMAND_HELP = "help"

# 权限
# 没有在此列出的权限皆为开放的权限
NET_PERMISSION_CREATE = 1
NET_PERMISSION_LOGIN = 1 << 1
NET_PERMISSION_LOGOUT = 1 << 2
NET_PERMISSION_CHAT = 1 << 3
NET_PERMISSION_ROLLSTART = 1 << 4
NET_PERMISSION_ROLL = 1 << 5
NET_PERMISSION_INFO = 1 << 6
permissionList = {
    NET_COMMAND_CHAT: NET_PERMISSION_CHAT,
    NET_COMMAND_CREATE: NET_PERMISSION_CREATE,
    NET_COMMAND_LOGIN: NET_PERMISSION_LOGIN,
    NET_COMMAND_LOGOUT: NET_PERMISSION_LOGOUT,
    NET_COMMAND_INFO: NET_PERMISSION_INFO,
    NET_COMMAND_ROLLSTART: NET_PERMISSION_ROLLSTART,
    NET_COMMAND_ROLL: NET_PERMISSION_ROLL
}
