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
NET_COMMAND_RESPONSE_CREATE_ARGS_AMOUNT_ERROR = "[Server] Create command arguments amount error!"
NET_COMMAND_RESPONSE_CREATE_USERNAME_EXISTED = "[Server] Username has existed, please try again!"
NET_COMMAND_RESPONSE_CREATE_SUCCESS = "[Server] Username create/register success!"

NET_COMMAND_LOGIN = "login"
NET_COMMAND_RESPONSE_LOGIN_ARGS_AMOUNT_ERROR = "[Server] Login command arguments amount error!"
NET_COMMAND_RESPONSE_LOGIN_PASSWORD_WRONG = "[Server] Your password is wrong, please retry!"
NET_COMMAND_RESPONSE_LOGIN_USERNAME_NOT_FOUND = "[Server] Username not found, please create first!"
NET_COMMAND_RESPONSE_LOGIN_IS_ONLINE = "[Server] This username has logged in!"
NET_COMMAND_RESPONSE_LOGIN_SUCCESS = "[Server] Welcome to our server!"

NET_COMMAND_LOGOUT = "logout"
NET_COMMAND_RESPONSE_LOGOUT_HAS_ARGS = "[Server] Logout command should not contain any arguments!"
NET_COMMAND_RESPONSE_LOGOUT_SUCCESS = "[Server] You quit from server!"

NET_COMMAND_CHAT = "chat"

NET_COMMAND_INFO = "info"
NET_COMMAND_RESPONSE_INFO_ARGS_AMOUNT_ERROR = "[Server] Info command arguments amount error!"
NET_COMMAND_RESPONSE_INFO_USER_NOT_FOUND = "[Server] User not found!"

NET_COMMAND_ROLL = "roll"
NET_COMMAND_RESPONSE_ROLL_ARGS_AMOUNT_ERROR = "[Server] Command roll should not get any arguments!"
NET_COMMAND_RESPONSE_ROLL_GAME_NOT_START = "[Server] Rollgame not start!"
NET_COMMAND_RESPONSE_ROLL_ONLY_ONCE = "[Server] You can roll only once!"

NET_COMMAND_ROLLSTART = "rollstart"
NET_COMMAND_RESPONSE_ROLLSTART_ARGS_AMOUNT_ERROR = "[Server] Command rollstart should get only 1 arguments!"
NET_COMMAND_RESPONSE_ROLLSTART_IS_PROGRESSING = "[Server] There has been another roll game progressing!"

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

# 网络传输目标
NET_MSG_TARGET_BROADCAST = -1  # 广播
