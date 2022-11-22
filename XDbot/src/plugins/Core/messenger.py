from . import __commands__ as commands
from nonebot.log import logger
import nonebot
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import nonebot.params
import json


@commands.messenger.handle()
async def _(
    event: nonebot.adapters.onebot.v11.event.MessageEvent,
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    args = str(message).split("\n")
    data = json.load(open("./data/XDbot/messenger/messenger.json"))
    try:
        data += [
            {
                "to": args[0].strip(),
                "message": str(message).replace(args[0], "").strip(),
                "sender": {
                    "id": event.get_user_id(),
                    "nick": event.sender.nickname
                }
            }
        ]
    except IndexError:
        await commands.messenger.finish("参数不足！", at_sender=True)
    except Exception as e:
        await commands.messenger.finish(f"未知错误：{e}", at_sender=True)
    else:
        json.dump(data, open("./data/XDbot/messenger/messenger.json", "w"))
        await commands.messenger.finish("已添加到信使队列", at_sender=True)


@commands.messenger_sender.handle()
async def _(event: nonebot.adapters.onebot.v11.event.MessageEvent):
    logger.info(event.sender.nickname)
    data = json.load(open("./data/XDbot/messenger/messenger.json"))
    length = 0
    qq = event.get_user_id()
    sent = []
    # 循环检查队列
    for dat in data:
        if dat["to"] == qq:
            await commands.messenger_sender.send(
                nonebot.adapters.onebot.v11.message.Message(
                    f"\n发信：{dat['sender']['nick']}({dat['sender']['id']})\n{dat['message']}"
                ),
                at_sender=True
            )
            sent += [length]
        length += 1
    # 删除已发
    length = 0
    for sent_id in sent:
        data.pop(sent_id - length)
        length += 1
    json.dump(data, open("./data/XDbot/messenger/messenger.json", "w"))
