import json
from . import __commands__ as commands
from . import __config__ as config
from . import __mysql__
import nonebot.adapters.onebot.v11.event
import random
import time


@commands.sign_command.handle()
@commands.sign_keyword.handle()
async def sign_handle(event: nonebot.adapters.onebot.v11.event.GroupMessageEvent):
    if event.get_plaintext() in ["签到", "/签到", "/sign"]:
        # 收集基础信息
        sign_data = json.load(open("./data/XDbot/sign_data.json"))
        qq = event.get_user_id()
        if qq not in sign_data.keys():
            sign_data[qq] = 0
        date = int(int(time.time()) / 86400)
        # 是否重复签到
        if sign_data[qq] < date:
            # 是否断签
            if sign_data[qq] == date - 1:
                checked_in = __mysql__.get_user_data(
                    int(qq), 4) + 1
            else:
                checked_in = 1
            # 奖励计算
            if checked_in >= 15:
                add_exp = 15
            else:
                add_exp = checked_in + 1
            add_coin = int(add_exp / 2) + random.randint(5, 15)
            # 保存数据
            sign_data[qq] = date
            __mysql__.add_coin_for_user(
                int(qq), add_coin)[2]
            level_update_data = __mysql__.add_exp_for_user(qq, add_exp)
            json.dump(sign_data, open("./data/XDbot/sign_data.json", "w"))
            __mysql__.set_user_data(int(qq), "checked_in", checked_in)
            # 返回结果
            if level_update_data:
                await commands.sign_command.send(f"""【等级提升】{level_update_data[2] - 1} -> {level_update_data[2]}""", at_sender=True)
            await commands.sign_command.finish(f"""签到成功！
您获得了 {add_exp} 经验和 {add_coin} {config.currency_symbol}
您已连续签到 {checked_in} 天""", at_sender=True)
        else:
            await commands.sign_command.finish("您已经签过到了！", at_sender=True)
