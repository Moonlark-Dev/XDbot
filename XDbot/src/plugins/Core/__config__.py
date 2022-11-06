import os

# Global Config
# 机器人昵称
bot_nickname: str = "XDbot"
# 程序版本，请不要修改此项
version: str = "1.9.5"


# Plugin Config
class translate:
    # 这里是作者的api_key，可自行前往木小果API申请（腾讯翻译）
    api_key: str = "0120dc0822bf4e67"


class ping:
    # 请求次数参数，默认自动获取
    if os.name == "nt":
        count_arg: str = "-n"
    else:
        count_arg: str = "-c"
    # 请求次数
    count: int = 4


class command_help:
    # 指令前缀
    command_start: str = "/"
    # 指令列表追加内容
    list_backhander: str = f"使用 {command_start}help <command> 获取更多信息"
