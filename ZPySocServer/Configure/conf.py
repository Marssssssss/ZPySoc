NET_STATE_STOP = 0
NET_STATE_CLOSING = 1
NET_STATE_CONNECTING = 2
NET_STATE_ESTABLISHED = 3

NET_TYPE_UNKNOWN = 0
NET_TYPE_SC = 1
NET_TYPE_CS = 2


# commands
# command method: $command params
# if '$' is in params string ,it should follow after \
# To last commit: if a command end with \, it should end with space
NET_COMMAND_CREATE = "create"
NET_COMMAND_LOGIN = "login"
NET_COMMAND_LOGOUT = "logout"
NET_COMMAND_CHAT = "chat"
NET_COMMAND_INFO = "info"

NET_COMMAND_ROLL = "roll"
NET_COMMAND_ROLLSTART = "rollstart"

NET_COMMAND_LIST = [
    NET_COMMAND_CREATE,
    NET_COMMAND_LOGIN,
    NET_COMMAND_LOGOUT,
    NET_COMMAND_CHAT,
    NET_COMMAND_INFO,
    NET_COMMAND_ROLL,
    NET_COMMAND_ROLLSTART
]
