from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
import json

messenger = on_command("messenger", aliases={"信使", "msg"})
sender = on_message()


@messenger.handle()
async def _(event: MessageEvent, message: Message = CommandArg()):
    args = str(message).split("\n")
    data = json.load(open("./data/messenger.json"))
    try:
        data += [
            {
                "to": args[0].strip(),
                "message": str(message).replace(args[0], "").strip(),
                "sender": {
                    "id": event.get_user_id(),
                    "nick": event.sender.card
                }
            }
        ]
    except IndexError:
        await messenger.finish("参数不足！", at_sender=True)
    except Exception as e:
        await messenger.finish(f"未知错误：{e}", at_sender=True)
    else:
        json.dump(data, open("./data/messenger.json", "w"))
        await messenger.finish("已添加到信使队列", at_sender=True)


@sender.handle()
async def _(bot: Bot, event: MessageEvent):
    data = json.load(open("./data/messenger.json"))
    length = 0
    qq = event.get_user_id()
    sent = []
    # 循环检查队列
    for dat in data:
        if dat["to"] == qq:
            await sender.send(
                Message(
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
    json.dump(data, open("./data/messenger.json", "w"))
