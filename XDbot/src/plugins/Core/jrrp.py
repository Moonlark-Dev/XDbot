from . import __commands__ as commands
import nonebot.adapters.onebot.v11.event
from nonebot.log import logger
import random
import time


@commands.jrrp.handle()
async def jrrp_handle(event: nonebot.adapters.onebot.v11.event.MessageEvent):
    qq = int(event.get_user_id())
    localtime = time.localtime(time.time())
    logger.info(qq)
    random.seed(
        qq * (localtime.tm_year + localtime.tm_mon + localtime.tm_mday))
    luck = random.randint(0, 100)

    if luck == 100:
        msg = "！100！！100！！！"
    elif luck == 99:
        msg = "，可惜不是100"
    elif 85 <= luck:
        msg = "，是不错的一天呢"
    elif 71 <= luck:
        msg = "，还行啦还行啦"
    elif 30 <= luck:
        msg = ""
    elif 29 <= luck:
        msg = "……"
    elif 15 <= luck:
        msg = "，呜哇——"
    elif 1 <= luck:
        msg = "，呜哇——（没错， 是百分制）"
    elif luck == 0:
        msg = "！0！！0！！！\n隐藏主题 非酋黑 已解锁，请前往 PCL114514 -> 设置 -> 个性化 中查看"
    else:
        msg = ""

    await commands.jrrp.finish(f"你今天的人品值是：{luck}{msg}", at_sender=True)
