import json
from . import __commands__ as commands
from . import __config__ as config
from . import __mysql__
import nonebot.adapters.onebot.v11.event
import random


@commands.sign_command.handle()
@commands.sign_keyword.handle()
async def sign_handle(event: nonebot.adapters.onebot.v11.event.GroupMessageEvent):
    signed = json.load(open("./data/XDbot/signed.json"))
    if event.get_user_id() not in signed:
        signed += [event.get_user_id()]
        checked_in = __mysql__.get_user_data(int(event.get_user_id()), 4) + 1
        if checked_in >= 15:
            add_exp = 15
        else:
            add_exp = checked_in + 1
        add_coin = int(add_exp / 2) + random.randint(5, 15)
        now_coin = __mysql__.add_coin_for_user(
            int(event.get_user_id()), add_coin)[2]
        old_level = __mysql__.get_user_data(int(event.get_user_id()), 1)
        is_level_update, now_exp, now_level = __mysql__.add_exp_for_user(
            int(event.get_user_id()), add_exp)

        json.dump(signed, open("./data/XDbot/signed.json", "w"))
        __mysql__.set_user_data(int(event.get_user_id()),
                                "checked_in", checked_in)
        if is_level_update:
            await commands.sign_command.send(f"""
「等级提升」
{old_level} -> {now_level}""", at_sender=True)
        await commands.sign_command.finish(f"""签到成功！
您获得了 {add_exp} 经验和 {add_coin} {config.currency_symbol}（当前拥有 {now_coin} {config.currency_symbol}）
您已连续签到 {checked_in} 天""", at_sender=True)
