from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

import requests
import os
import time
import asyncio
from playwright.async_api import async_playwright

geturl = on_command("get",aliases={"next-get"})

async def get_screenshot(url) -> None:
    try:
        async with await async_playwright() as p:
            browser = await p.firefox.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path = "./data/geturl.png", full_page = True)
            await browser.close()
    except:
        os.system(f"python html2png.py {url} geturl")


async def get(url):
    try:
        start_time = time.time()
        req = requests.get(url)
        end_time = time.time()
    except Exception as e:
        await geturl.finish(str(e))
    else:
        try: os.remove("./data/geturl.png")
        except: pass
        await get_screenshot(url)
        answer = f"""请求结果：
URL: {req.url}
状态：{req.status_code}
耗时：{end_time - start_time}s
"""
        answer += MessageSegment.image("file:///C:/Users/ITCS/Desktop/XDbot.Core/data/geturl.png")
        await geturl.finish(Message(answer))
        


@geturl.handle()
async def geturl_handle(bot: Bot, event: MessageEvent, message:Message = CommandArg()):
    asyncio.create_task(get(message))
    await geturl.send(f"正在请求 {message}，请稍候")
	
	
