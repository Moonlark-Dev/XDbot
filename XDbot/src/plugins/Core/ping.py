from . import __config__ as config
from . import __commands__ as commands
import nonebot.adapters.onebot.v11.message
import nonebot.adapters
import nonebot.params
import asyncio

"""
class new_stdout:
    def __init__(self):
        self.print_text = ""

    def write(self, text):
        self.print_text += text
        logger.info(text)
    
    def fileno(self):
        pass

    def flush(self):
        pass

    def get(self):
        return self.print_text
"""


async def ping(url):
    cmd = await asyncio.create_subprocess_shell(f"ping \"{url}\" {config.ping.count_arg} {config.ping.count}", stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    text = stdout.decode()
    answ = text.split("\n\n")[1]
    await commands.ping.finish("\n" + answ, at_sender=True)


async def ping_full_log(url):
    # cmd  = os.popen(f"ping \"{url}\" {count_arg} 4")
    # text = cmd.read()
    # await commands.ping_full_log.finish("\n" + text, at_sender = True)
    cmd = await asyncio.create_subprocess_shell(f"ping \"{url}\" {config.ping.count_arg} {config.ping.count}", stdin=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await cmd.communicate()
    text = stdout.decode()
    await commands.ping_full_log.finish("\n" + text, at_sender=True)


@commands.ping.handle()
async def ping_handle(
    args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()
):
    await commands.ping.send(
        f"正在 PING {args}，请稍候", at_sender=True)
    asyncio.create_task(ping(args))


@commands.ping_full_log.handle()
async def ping_full_log_handle(
    args: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()
):
    await commands.ping_full_log.send(
        f"正在 PING {args}，请稍候", at_sender=True)
    asyncio.create_task(ping_full_log(args))
