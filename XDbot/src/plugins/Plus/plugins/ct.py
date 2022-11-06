from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.log import logger
import json

write = on_message()
ct = on_command("ct")
mct = on_command("mct")
mctg = on_command("mctg")
ctg = on_command("ctg")


@write.handle()
async def _(bot: Bot, event: MessageEvent):
    data = json.load(open("./data/ct.json"))
    qq = event.get_user_id()
    group = event.get_session_id().split("_")[1]

    try:
        data["global"][qq] += 1
    except KeyError:
        data["global"][qq] = 1

    try:
        data[group][qq] += 1
    except KeyError:
        try:
            data[group][qq] = 1
        except KeyError:
            data[group] = {qq: 1}
    json.dump(data, open("./data/ct.json", "w"))


@ct.handle()
async def _(bot: Bot, event: MessageEvent):
    qq = event.get_user_id()
    group = event.get_session_id().split("_")[1]
    config = json.load(open("./data/ct.json"))
    logger.info(config)

    await ctg.send("正在获取排名信息，请稍候", at_sender=True)

    users = []
    mylength = 0
    for key in list(config[group].keys()):
        logger.info(users)

        length = 0
        insert = False
        for user in users:
            if user["count"] <= config[group][key]:
                users.insert(
                    length,
                    {
                        "id": key,
                        "count": config[group][key]
                    }
                )
                insert = True
                if key == qq:
                    mylength = length + 1
                break
            else:
                length += 1
        if not insert:
            users += [{
                "id": key,
                "count": config[group][key]
            }]
            if key == qq:
                mylength = length
    answer = f"发言排名 —— {group}\n"
    length = 1
    for user in users[0:10]:
        # req    =  requests.get(f"https://api.usuuu.com/qq/{user['id']}")
        qqnick = (await bot.get_stranger_info(user_id=user['id']))['nickname']
        answer += f"{length}. {qqnick}: {user['count']}\n"
        length += 1

    length = 1
    for user in users:
        if user["id"] == qq:
            mylength = length
            break
        else:
            length += 1

    # req    =  requests.get(f"https://api.usuuu.com/qq/{qq}")
    qqnick = (await bot.get_stranger_info(user_id=user['id']))['nickname']
    answer += f"""-----------------------------
{mylength}. {qqnick}: {config[group][qq]}"""
    await ct.finish(answer)


@mct.handle()
async def _(bot: Bot, event: MessageEvent, message: Message = CommandArg()):
    argv = str(message)
    group = event.get_session_id().split("_")[1]
    if argv != "":
        qq = argv.replace("[CQ:at,qq=", "").replace("]", "")
    else:
        qq = event.get_user_id()
    config = json.load(open("./data/ct.json"))
    logger.info(config)

    users = []
    mylength = 0
    for key in list(config[group].keys()):
        logger.info(users)

        length = 0
        insert = False
        for user in users:
            if user["count"] <= config[group][key]:
                users.insert(
                    length,
                    {
                        "id": key,
                        "count": config[group][key]
                    }
                )
                insert = True

                break
            else:
                length += 1
        if not insert:
            users += [{
                "id": key,
                "count": config[group][key]
            }]
    length = 1
    for user in users:
        if user["id"] == qq:
            mylength = length
            break
        else:
            length += 1

    try:
        await ct.finish(f"""发言数据 —— {group}
用户：{qq}
排名：{mylength}（总数：{users.__len__()}）
发言量：{config[group][qq]}""")
    except KeyError:
        await ct.finish("暂无数据", at_sender=True)


@ctg.handle()
async def _(bot: Bot, event: MessageEvent):
    qq = event.get_user_id()
    config = json.load(open("./data/ct.json"))
    logger.info(config)

    await ctg.send("正在获取排名信息，请稍候", at_sender=True)

    users = []
    mylength = 0
    for key in list(config["global"].keys()):
        logger.info(users)

        length = 0
        insert = False
        for user in users:
            if user["count"] <= config["global"][key]:
                users.insert(
                    length,
                    {
                        "id": key,
                        "count": config["global"][key]
                    }
                )
                insert = True

                break
            else:
                length += 1
        if not insert:
            users += [{
                "id": key,
                "count": config["global"][key]
            }]
    answer = "发言排名 —— 全局\n"
    length = 1
    for user in users[0:10]:
        # req    =  requests.get(f"https://api.usuuu.com/qq/{user['id']}")
        qqnick = (await bot.get_stranger_info(user_id=user["id"]))["nickname"]
        answer += f"{length}. {qqnick}: {user['count']}\n"
        length += 1

    length = 1
    for user in users:
        if user["id"] == qq:
            mylength = length
            break
        else:
            length += 1
    # req    =  requests.get(f"https://api.usuuu.com/qq/{qq}")
    qqnick = (await bot.get_stranger_info(user_id=user["id"]))["nickname"]
    answer += f"""-----------------------------
{mylength}. {qqnick}: {config['global'][qq]}"""
    await ctg.finish(answer)


@mctg.handle()
async def _(bot: Bot, event: MessageEvent, message: Message = CommandArg()):
    argv = str(message)
    if argv != "":
        qq = argv.replace("[CQ:at,qq=", "").replace("]", "")
    else:
        qq = event.get_user_id()
    config = json.load(open("./data/ct.json"))
    logger.info(config)

    users = []
    mylength = 0
    for key in list(config["global"].keys()):
        logger.info(users)

        length = 0
        insert = False
        for user in users:
            if user["count"] <= config["global"][key]:
                users.insert(
                    length,
                    {
                        "id": key,
                        "count": config["global"][key]
                    }
                )
                insert = True
                break
            else:
                length += 1
        if not insert:
            users += [{
                "id": key,
                "count": config["global"][key]
            }]
    length = 1
    for user in users:
        if user["id"] == qq:
            mylength = length
            break
        else:
            length += 1
    try:
        await ctg.finish(f"""发言数据 —— 全局
用户：{qq}
排名：{mylength}（总数：{users.__len__()}）
发言量：{config['global'][qq]}""")
    except KeyError:
        await ctg.finish("暂无数据", at_sender=True)
