from . import __commands__ as commands
from nonebot.log import logger
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11
import pyautogui
import os.path
import os


# Init
logger.info("Trying to take screenshots . . .")
pyautogui.screenshot("./data/XDbot/screenshot.png")
    


@commands.screenshot.handle()
async def screenshot_handle():
    if os.path.isfile("./data/XDbot/screenshot.png"):
        os.remove("./data/XDbot/screenshot.png")
    pyautogui.screenshot("./data/XDbot/screenshot.png")
    await commands.screenshot.finish(
        nonebot.adapters.onebot.v11.Message(
            nonebot.adapters.onebot.v11.message.MessageSegment.image(
                f"file:///{os.path.abspath('')}/data/XDbot/screenshot.png")))
