from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.log import logger


echo = on_command("echo")

@echo.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    await echo.finish(args)
	

execute = on_command("execute", permission = SUPERUSER)

@execute.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    try:
        logger.info(f"Execute: {args}")
        await execute.finish(str(eval(str(args))))
	
    except Exception as e:
        logger.warning(f"Error: {e}")
        await execute.finish(f"{e}")
