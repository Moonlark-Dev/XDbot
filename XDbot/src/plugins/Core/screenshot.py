from . import __commands__ as commands
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11
import pyautogui
import os.path
import os


@commands.screenshot.handle()
async def screenshot_handle():
    if os.path.isfile("./data/screenshot.png"):
        os.remove("./data/screenshot.png")
    pyautogui.screenshot("./data/screenshot.png")
    await commands.screenshot.finish(
        nonebot.adapters.onebot.v11.Message(
            nonebot.adapters.onebot.v11.message.MessageSegment.image(
                f"file:///{os.path.abspath('')}/data/screenshot.png")))
