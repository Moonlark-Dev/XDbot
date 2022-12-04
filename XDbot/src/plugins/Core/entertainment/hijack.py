import json
from . import __commands__ as commands
from . import __config__ as config
from . import __mysql__
import nonebot.adapters.onebot.v11.event
import nonebot.adapters.onebot.v11
import nonebot.params
import random


@commands.hijack_command.handle()
async def hijack_handle(
        event: nonebot.adapters.onebot.v11.event.GroupMessageEvent,
        message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
        ):
    # Rand = random.randint()
    try :
        args = str(message).split("\n")
        ID = event.get_user_id()
        coins = int(__mysql__.get_user_data(int(args[0]), 3) / 10) # Get 1 / 10
        Rand = random.randint(0, coins)
        __mysql__.add_coin_for_user(args[0], 0-Rand)
        __mysql__.add_coin_for_user(ID, Rand)
        await commands.guessnum.finish(f"你已成功打劫他{Rand} VimCoin!")
    except ValueError:
        await commands.guessnum.finish(f"""未知：{args[0]}"""}
