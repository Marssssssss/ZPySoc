# --coding=utf-8--
# 全指令 tips
NET_HELP_TIPS_ALL = "[Server] Some command used below:\n" \
                    "        $create username password (to register in the server)\n" \
                    "        $login username password  (to login the server)\n" \
                    "        $logout                   (to logout the server)\n" \
                    "        $chat words               (if you need to use $, use \\$ instead)\n" \
                    "        $info UserA               (get other's user info)\n" \
                    "        $rollstart keepTimes      (to start a roll game which will end in keepTimes secs, " \
                                                       "keepTimes <= 300)\n" \
                    "        $roll                     (to roll a number when a roll game progesses)\n"\
                    "        $help [command]           (To get help!)"

# 单指令 tips
NET_HELP_TIPS_HEAD = "[Server] Command you want to know:\n"
NET_HELP_TIPS_UNKNOWN_HEAD = "         => Unknown command:"

NET_HELP_TIP_HELP = "help"

tipsForSingleCommand = {
    NET_HELP_TIP_HELP: "$help [command] (To get help!)"
}