from . import __commands__ as commands
from nonebot.log import logger
import nonebot.adapters.onebot.v11.message
import nonebot.params


@commands.echo.handle()
async def echo_handle(args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()):
    await commands.echo.finish(nonebot.adapters.onebot.v11.message.Message(args))


@commands.execute.handle()
async def execute_handle(args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()):
    try:
        logger.info(f"Execute: {args}")
        await commands.execute.finish(str(eval(str(args))))

    except Exception as e:
        logger.warning(f"Error: {e}")
        await commands.execute.finish(f"{e}")
