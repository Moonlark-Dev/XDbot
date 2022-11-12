from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.log import logger

import pyautogui

screenshot = on_command("screenshot")

@screenshot.handle()
async def _(bot: Bot, event: MessageEvent, message: Message = CommandArg()):
    pyautogui.screenshot("./data/screenshot.png")
    await screenshot.finish(Message(MessageSegment.image("file:///C:/Users/ITCS/Desktop/XDbot.Core/data/screenshot.png")))
