from .. import __config__

# Global Config
# 机器人昵称
bot_nickname: str = __config__.bot_nickname
# 程序版本，请不要修改此项
version: str = __config__.version
# 货币符号
# 默认的别问，问就是随机出来的（
currency_symbol: str = "vi"
# 货币名称
currency_name: str = "VimCoin"


# MYSQL
class mysql:
    host: str = "web.xiexilin.cn"
    user: str = "root"
    passwd: str = "091113Dsh"
    database: str = "XDBOT"
    table: dict = {
        "users": "Users",
        "items": "Items"
    }


# Plugin Config
class guessnum:
    # Number 请不要修改此项
    number: dict = {}
    # 最大值
    max: int = 250
    # 限时，单位秒
    max_time: float = 60.0
    # 最后一次触发
    latest_create: dict = {}


class randomDrop:
    # 全局概率
    global_probability: float = 0.05
    # 物品概率
    probability: list = [
        {"id": 7, "count": 10, "probability": 0.25},
        {"id": 8, "count": 15, "probability": 0.50},
        {"id": 2, "count": 5, "probability": 0.20},
        {"id": 4, "count": 1, "probability": 0.03},
        {"id": 5, "count": 1, "probability": 0.02}
    ]
