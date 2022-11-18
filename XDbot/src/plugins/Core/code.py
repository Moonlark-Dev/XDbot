from . import __config__ as config
from . import __commands__ as commands
from nonebot.log import logger
import nonebot.adapters.onebot.v11.message
import nonebot.params
import httpx
import json
import traceback


async def run_code(code, language, stdin):
    """
    Run code in the specified language.

    :param code: code to run
    :type code: str
    :param language: language to run code in
    :type language: str
    :param stdin: stdin to run code in
    """
    send_json = {
        "files": [
            {"name": "main", "content": code}
        ],
        "stdin": stdin
    }
    logger.info(send_json)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://glot.io/api/run/{language}/latest",
                headers=config.code.header,
                data=json.dumps(send_json)
            )
            logger.info("done")
        except Exception:
            logger.error(traceback.format_exc())
            return await commands.code.finish(str(traceback.format_exc()))
        data = json.loads(response.read())
        if "message" in data.keys():
            return await commands.code.finish(data["message"])
        elif not (data["error"] or data["stderr"]):
            return await commands.code.finish(data["stdout"])
        else:
            return await commands.code.finish(f'ERROR: {data["error"]}\n{data["stderr"]}')
        


@commands.code.handle()
async def code_handle(
    message: nonebot.adapters.onebot.v11.message.Message = nonebot.params.CommandArg()):
    """
    Handle code
    """
    args = str(message)
    if not args:
        return await commands.code.finish("参数不足")
    code = args[args.find("\n")+1:]
    language = args.split("\n")[0].split(" ")[0]
    if args.split("\n")[0].find("-i") != -1:
        stdin = args.split("\n")[0].replace("-i", "").replace(language, "").strip()
    else:
        stdin = ""
    logger.info(f"code: {code}")
    logger.info(f"stdin: {stdin}")
    logger.info(f"language: {language}")
    try:
        await run_code(code, language, stdin)
    except Exception:
        logger.error(traceback.format_exc())
        # await commands.code.finish(traceback.format_exc())