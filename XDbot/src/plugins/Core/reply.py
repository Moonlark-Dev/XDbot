from . import __commands__ as commands
from . import __config__ as config
from nonebot.log import logger
import nonebot.adapters.onebot.v11.bot
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import json
import nonebot.params
import os.path
import os
import random
import time
import httpx


@commands.to_me.handle()
async def to_me_handle():
    if random.random() <= 0.10:
        await commands.to_me.send("？")

"""
async def download(url, name):
    Download file from url and save to fname
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        with open(f"./data/XDbot/reply_images/{name}", "wb") as f:
            f.write(response.read())
    logger.success(f"Saved {url} to {name}.")


async def get_image_url(cqcode):
    url_start = cqcode.find("url=") + 4
    if cqcode.find(",", url_start) != -1:
        url_end = cqcode.find(",", url_start)
    else:
        url_end = cqcode.find("]")
    try:
        await download(cqcode[url_start:url_end], str(int(time.time())) + ".png")
    except Exception as e:
        logger.warning(f"Cannot download {cqcode[url_start:url_end]}: {e}")


async def get_image_cqcode(message, start_search=0):
    cqcode_start = message.find("CQ:image", start_search)
    if cqcode_start != -1:
        cqcode_end = message.find("]", cqcode_start)
        await get_image_url(message[cqcode_start:cqcode_end])
        return get_image_cqcode(message, cqcode_end)
    else:
        return
"""

def get_num_of_repetion(string: str, text: str, start: int = 0):
    size = string.find(text, start)
    if size == -1:
        return 0
    elif len(string) != size + 1:
        return 1 + get_num_of_repetion(string, text, size + 1)
    else:
        return 0


@commands.random_save_pic.handle()
async def random_save_pictrue(
    bot: nonebot.adapters.onebot.v11.bot.Bot,
    event: nonebot.adapters.onebot.v11.event.MessageEvent
):
    message = str(event.get_message())
    data = json.load(open("./data/XDbot/reply.json"))


    # logger.info(get_num_of_repetion(message, "[CQ:image"))
    if get_num_of_repetion(message, "[CQ:image") == 1\
            and message.find("subType=1") != -1\
            and message.find("[CQ:image") == 0\
            and message[-1] == "]"\
            and random.random() <= 0.05:
        # logger.info(f"Downloading images in {message}")
        image_id = str(len(data["review"].keys()))
        data["review"][image_id] = [message]
        await bot.send_group_msg(message=f"{message}来自{event.get_session_id().split('_')[1]}的{event.sender.user_id}\n使用 {config.command_help.command_start}img y {image_id} 通过\n使用 {config.command_help.command_start}img n {image_id} 删除", group_id=config.reply.review_group)
        json.dump(data, open("./data/XDbot/reply.json", "w"))
        await commands.random_save_pic.send("好图，我的了")


@commands.img_admin.handle()
async def img_admin_handle(
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    data = json.load(open("./data/XDbot/reply.json"))
    args = str(message).split(" ")
    if args[0] == "y":
        data["data"].append(data["review"].pop(args[1]))
    elif args[0] == "n":
        data["review"].pop(args[1])
    elif args[0] == "w":
        review_list = data["review"]
        for image in review_list.keys():
            await commands.img_admin.send(nonebot.adapters.onebot.v11.Message(f"ID: {image}\n{review_list[image][0]}"))
    elif args[0] == "r":
        data["data"].pop(int(args[1]))
    elif args[0] == "l":
        length = 0
        for image in data["data"]:
            await commands.img_admin.send(message=nonebot.adapters.onebot.v11.Message(f"ID: {length}\n{image}"))
            length += 1
    elif args[0] == "a":
        data["data"].append(args[1])
    elif args[0] == "p":
        image_keys = data["review"].copy().keys()
        for image_id in image_keys:
            data["data"].append(data["review"].pop(image_id))
    json.dump(data, open("./data/XDbot/reply.json", "w"))
    await commands.img_admin.finish("完成")


@commands.random_send_pic.handle()
async def random_send_pictrue():
    if random.random() <= 0.05 and time.time() - \
            config.reply.latest_send >= config.reply.send_sleep:
        config.reply.latest_send = time.time()
        images = json.load(open("./data/XDbot/reply.json"))

        if random.random() <= 0.15 and images["data"].__len__() > 20:
            images["data"] = images["data"][-int(len(images["data"]) / 2):]
            json.dump(images, open("./data/XDbot/reply.json"))

        image = random.choice(images["data"])
        await commands.random_send_pic.send(
            nonebot.adapters.onebot.v11.Message(
                image
            )
        )
