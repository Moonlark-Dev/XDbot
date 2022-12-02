from nonebot.log import logger
from . import __commands__ as commands
import nonebot.adapters.onebot.v11
import nonebot.params
import httpx
import time


async def get(url):
    logger.info(f"URL: {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code


@commands.geturl.handle()
async def geturl_handle(message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()):
    url = str(message)
    await commands.geturl.send(f"正在请求 {url}，请稍候")
    try:
        start_time = time.time()
        status_code = await get(url)
        end_time = time.time()
    except Exception as e:
        return await commands.geturl.finish(str(e))
    answer = f"""请求结果：
URL: {url}
状态：{status_code}
耗时：{end_time - start_time}s
"""
    await commands.geturl.finish(answer)
