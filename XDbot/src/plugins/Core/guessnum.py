from . import __commands__ as commands
from . import __config__ as config
from nonebot.log import logger
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import nonebot.params
import random
import asyncio


async def autoremove(bot, sleep_time, group):
    await asyncio.sleep(sleep_time)
    if group in list(config.guessnum.number.keys()):
        await bot.send(f"时间到，游戏结束，正确答案：{config.guessnum.number[group]}")
        config.guessnum.number.pop(group)


@commands.guessnum.handle()
async def guessnum_handle(
        event: nonebot.adapters.onebot.v11.event.MessageEvent,
        message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
    ):
    argv = message.extract_plain_text().split(" ")
    group = event.get_session_id().split("_")[1]
    # Start Game
    if argv[0] == "start":
        if group not in config.guessnum.number.keys():
            config.guessnum.number[group] = random.randint(0, config.guessnum.max)
            logger.info(f"Created game in group {group}, answer {config.guessnum.number[group]}")
            await commands.guessnum.finish(f"【猜数字】：游戏已创建，请在60秒内使用 /guess <number> 作答，取值范围 0 <= <number> <= {config.guessnum.max}")
            asyncio.create_task(autoremove(commands.guessnum, 60000, config.guessnum.max))
        else:
            await commands.guessnum.finish("游戏已存在")
    # Ranking
    elif argv[0] == "list":
        await commands.guessnum.finish("敬请期待")
    # Stop Game
    elif argv[0] == "stop":
        try:
            answer = config.guessnum.number.pop(group)
        except KeyError:
            await commands.guessnum.finish("找不到游戏", at_sender = True)
        else:
            await commands.guessnum.finish(f"游戏结束，正确答案：{answer}")
    else:
        # Guess number
        try:
            guessed = int(argv[0])
            if guessed == config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，回答正确！", at_sender = True)
                config.guessnum.number.pop(group)
            elif guessed > config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，大了", at_sender = True)
            elif guessed < config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，小了", at_sender = True)
        except KeyError:
            await commands.guessnum.finish("游戏未开始或已结束，使用 /guess start 创建游戏", at_sender = True)
