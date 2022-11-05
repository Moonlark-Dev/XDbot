from . import __commands__ as commands
from . import __config__ as config
from nonebot.log import logger
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11

logger.info(f"Welcome to use XDbot V{config.version}!")


@commands.about.handle()
async def about_handle():
    answer = f"""XDbot  (This-is-XiaoDeng/XDbot)
Copyright (c) 2022 This is XiaoDeng
Version {config.version}"""
    answer += nonebot.adapters.onebot.v11.message.MessageSegment.image(
        "https://itcdt.top/file/QQ_Image_1664966405883.jpg")
    await commands.about.finish(nonebot.adapters.onebot.v11.Message(answer))
