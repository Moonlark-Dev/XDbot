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
    output = ""
    try:
        msg = message.extract_plain_text().split(" ")
        output = items.use_item(event.get_user_id(), int(msg[0]), int(msg[1]))
    except ValueError:
        await commands.use_item.send("无效参数")
    except IndexError:
        await commands.use_item.send("索引失败")
    except Exception as e:
        await commands.use_item.send(f"未知错误：{e}")
    for out in output:
        await commands.use_item.send(out)


@commands.get_bag.handle()
async def get_bag_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent,
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    qq = event.get_user_id()
    msg = message.extract_plain_text().split(" ")
    # print(msg)
    if msg == [""]:
        answer = f"{qq}的背包："
        bag = items.get_user_bag(qq)
        length = 0
        for item in bag:
            answer += f"\n[{length}] {items.get_item(item['id'])[1]} x{item['count']}"
            if item["data"] != {}:
                answer += " (NBT)"
        await commands.get_bag.finish(answer)
    elif msg[0] == "view":
        # answer = ""
        bag = items.get_user_bag(qq)
        item = bag[int(msg[1])]
        if "name" in item["data"].keys():
            name = item["data"]["name"]
        else:
            name = items.get_item(item["id"])[1]
        answer = f"「{name}」\n当前拥有：{item['count']}\n{items.get_item(item['id'])[2]}"
        for nbt in item["data"].keys():
            if nbt == "info":
                answer += f"\n\t\n{item['data']['info']}"
        await commands.get_bag.finish(nonebot.adapters.onebot.v11.Message(answer))


@commands.list_items.handle()
async def list_item_handle():
    answer = "【物品列表】\n"
    item_list = items.get_items()
    # length = 1
    for item in item_list:
        answer += f"""「{item[1]}」(ID: {item[0]})
    [{item[3]}] {item[2]}\n"""
    await commands.get_bag.finish(answer)


@commands.give_item.handle()
async def give_item_handle(
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    msg = message.extract_plain_text().split(" ")
    to_user = msg[0].replace("[CQ:at,qq=", "").replace("]", "")
    item_id = int(msg[1])
    if len(msg) >= 3:
        count = int(msg[2])
    else:
        count = 1
    if len(msg) >= 4:
        nbt = json.loads(msg[3].replace("%20", " "))
    else:
        nbt = {}
    if items.give_user_item(to_user, item_id, count, nbt):
        await commands.give_item.finish("完成")
    else:
        await commands.give_item.finish("失败")
