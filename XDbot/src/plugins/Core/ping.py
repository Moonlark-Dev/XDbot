from . import __commands__ as commands
import nonebot.adapters.onebot.v11.message
import nonebot.adapters
import nonebot.params
import os
import asyncio


async def ping(url):
    cmd  = os.popen(f"ping \"{url}\"")
    text = cmd.read()
    answ = text.split("\n\n")[1]
    await commands.ping.finish("\n" + answ, at_sender = True)

async def ping_full_log(url):
    cmd  = os.popen(f"ping \"{url}\"")
    text = cmd.read()
    await commands.ping_full_log.finish("\n" + text, at_sender = True)


@commands.ping.handle()
async def ping_handle(
    args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()
):
    await commands.ping.send(
        f"正在 PING {args}，请稍候", at_sender = True)
    asyncio.create_task(ping(args))


@commands.ping_full_log.handle()
async def ping_full_log_handle(
    args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()
):
    await commands.ping_full_log.send(
        f"正在 PING {args}，请稍候", at_sender = True)
    asyncio.create_task(ping_full_log(args))  
