from . import __commands__ as commands
import nonebot.permission
import nonebot.adapters.onebot.v11.message
import nonebot.params
import os
import asyncio



@commands.system.handle()
async def system_handle(args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()):
    command = args.extract_plain_text()
    cmd = await asyncio.create_subprocess_shell(command, stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    text = "[stdout]\n" + stdout.decode() + "\n[stderr]\n" + stderr.decode()
    await commands.system.finish(text)
