from . import __commands__ as commands
from nonebot.log import logger
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import os.path
import os
import random
import time
import httpx


async def download(url, name):
    """Download file from url and save to name"""
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


async def get_image_cqcode(message, start_search = 0):
    cqcode_start = message.find("CQ:image", start_search)
    if cqcode_start != -1:
        cqcode_end = message.find("]", cqcode_start)
        await get_image_url(message[cqcode_start:cqcode_end])
        return get_image_cqcode(message, cqcode_end)
    else:
        return


@commands.random_save_pic.handle()
async def random_save_pictrue(
        event: nonebot.adapters.onebot.v11.event.MessageEvent
    ):
    message = str(event.get_message())
    if message.find("CQ:image") != -1 and random.random() > 0.75:
        logger.info(f"Downloading images in {message}")
        await get_image_cqcode(message)
        await commands.random_send_pic.send("好图，我的了（")


@commands.random_send_pic.handle()
async def random_send_pictrue():
    if random.random() <= 0.20:
        images = os.listdir("./data/XDbot/reply_images")
        image = random.choice(images)
        image_path = os.path.abspath(f"./data/XDbot/reply_images/{image}")
        await commands.random_send_pic.send(
            nonebot.adapters.onebot.v11.Message(
                nonebot.adapters.onebot.v11.message.MessageSegment.image(
                    file=f"file://{image_path}"
                )
            )
        )
