from .. import __config__
import time
import os

# Global Config
# 机器人昵称
bot_nickname: str = __config__.bot_nickname
# 程序版本，请不要修改此项
version: str = __config__.version


# Plugin Config
class guessnum:
    # Number 请不要修改此项
    number: dict = {}
    # 最大值
    max: int = 250
    # 限时，单位秒
    max_time: float = 60.0
