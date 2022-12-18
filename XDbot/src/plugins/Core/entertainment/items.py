import json
from . import __commands__ as commands
from . import __items__ as items
import nonebot.adapters.onebot.v11.event
import random
import time
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import nonebot.params


@commands.use_item.handle()
async def use_item_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent,
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    try:
        msg = message.extract_plain_text().split(" ")
        output = items.use_item(event.get_user_id(), int(msg[0]), int(msg[1]))
    except ValueError:
        await commands.use_item.finish("无效参数")
    except IndexError:
        await commands.use_item.finish(f"索引失败")
    except Exception as e:
        await commands.use_item.finish(f"未知错误：{e}")
    else:
        for out in output:
            await commands.use_item.send(out)


@commands.get_bag.handle()
async def get_bag_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent
):
    qq = event.get_user_id()
    answer = f"{qq}的背包："
    bag = items.get_user_bag(qq)
    length = 0
    for item in bag:
        answer += f"\n  [{length}] {items.get_item(item['id'])[1]} x{item['count']}"
        if item["data"] != {}:
            answer += " (NBT)"
    await commands.get_bag.finish(answer)
