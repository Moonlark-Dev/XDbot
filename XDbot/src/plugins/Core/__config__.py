import time
import os

# Global Config
# 机器人昵称
bot_nickname: str = "XDbot"
# 程序版本，请不要修改此项
version: str = "2.3.5"


# Plugin Config
class translate:
    # 这里是作者的api_key，可自行前往木小果API申请（腾讯翻译）
    api_key: str = "0120dc0822bf4e67"


class code:
    # Token
    token: str = "a238bd14-14ae-43e4-a7ea-8942edd9b98c"
    # Header
    header: dict = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }


class guessnum:
    # Number 请不要修改此项
    number: dict = {}
    # 最大值
    max: int = 250



class cave:
    # 冷却时间，0为无限制
    sleep: int = 0
    # 最后一次随机时间
    latest_get: float = time.time()
    # 被删除的cave内容将被替换为此项目
    removed: str = "[Removed]"
    # MySQL 数据库设置
    host: str = "localhost"
    user: str = "root"
    password: str = ""
    database: str = "xdbot"
    table: str = "cave"
    # MySQL语句设置
    get_all_id: str = f"SELECT ID FROM {table} WHERE (MSG != '{removed}')"
    get_cave: str = f"SELECT * FROM {table} WHERE (ID = %ID%)" 
    

class cave_reply:
    # MySQL 数据库设置
    host: str = cave.host
    user: str = cave.user
    password: str = cave.password
    database: str = cave.database
    table: str = cave.table + "_reply"



class email:
    # 最后一次发件时间
    latest_send: float = time.time()
    # 冷却时间，单位秒（为 0 不限制）
    send_sleep: int = 90
    # 邮箱 Smtp 服务器
    smtp_server_host: str = ""
    smtp_server_port: int = 25
    # 邮箱帐号
    smtp_user: str = ""
    # 邮箱密码
    smtp_passwd: str = ""


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

class preview:
    # 测试playwright是否可用
    test_playwright: bool = True
