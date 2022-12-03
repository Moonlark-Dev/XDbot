from .. import __config__

# Global Config
# 机器人昵称
bot_nickname: str = __config__.bot_nickname
# 程序版本，请不要修改此项
version: str = __config__.version
# 货币符号
# 默认的别问，问就是随机出来的（
currency_symbol: str = "VI"


# MYSQL
class mysql:
    host: str = "localhost"
    user: str = "root"
    passwd: str = "091113Dsh"
    database: str = "XDBOT"
    table: dict = {
        "users": "Users"
    }


# Plugin Config
class guessnum:
    # Number 请不要修改此项
    number: dict = {}
    # 最大值
    max: int = 250
    # 限时，单位秒
    max_time: float = 60.0
