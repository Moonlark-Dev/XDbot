from . import __commands__ as commands
from . import __config__ as config
from . import __mysql__
from nonebot.log import logger
import traceback
import nonebot.adapters.onebot.v11
import nonebot.adapters.onebot.v11.event
import nonebot.params
import random
import asyncio
import time


async def autoremove(group):
    await asyncio.sleep(config.guessnum.max_time)
    logger.info(f"Stopping the game in {group}")
    if group in list(config.guessnum.number.keys()):
        await commands.guessnum.send(f"时间到，游戏结束，正确答案：{config.guessnum.number[group]}")
        config.guessnum.number.pop(group)


@commands.guessnum_onmsg.handle()
async def guessnum_onmessage_handle(
    event: nonebot.adapters.onebot.v11.event.GroupMessageEvent
):
    argv = event.get_plaintext()
    group = event.get_session_id().split("_")[1]
    if group in list(config.guessnum.number.keys()):
        # Guess number
        try:
            guessed = int(argv)
            if guessed == config.guessnum.number[group]:
                # Add coin
                coin = __mysql__.add_coin_for_user(
                    int(event.get_user_id()), random.randint(0, 10))[1]
                level_update_data = __mysql__.add_exp_for_user(
                    int(event.get_user_id()), 2)

                if level_update_data[0]:
                    await commands.guessnum.send(f"【等级提升】{level_update_data[2] - 1} -> {level_update_data[2]}", at_sender=True)

                # Finish
                answer = config.guessnum.number.pop(group)
                await commands.guessnum_onmsg.finish(f"{answer}，回答正确！\n你获得了 {coin} {config.currency_symbol}", at_sender=True)
            elif guessed > config.guessnum.number[group]:
                await commands.guessnum_onmsg.finish(f"{guessed}，大了", at_sender=True)
            elif guessed < config.guessnum.number[group]:
                await commands.guessnum_onmsg.finish(f"{guessed}，小了", at_sender=True)
        except Exception:
            logger.error(traceback.format_exc())


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
            if group in config.guessnum.latest_create.keys():
                if time.time() - \
                        config.guessnum.latest_create[group] <= config.guessnum.max_time:
                    return await commands.guessnum.finish(f"冷却中，请稍候！")
            config.guessnum.latest_create[group] = time.time()
            if __mysql__.get_user_data(int(event.get_user_id()), 3) >= 1:
                __mysql__.add_coin_for_user(int(event.get_user_id()), -1)
            else:
                return await commands.guessnum.finish(f"{config.currency_name} 不足")
            config.guessnum.number[group] = random.randint(
                0, config.guessnum.max)
            logger.info(
                f"Created game in group {group}, answer {config.guessnum.number[group]}")
            asyncio.create_task(autoremove(group))
            await commands.guessnum.finish(f"【猜数字】：请在 {config.guessnum.max_time}s 内作答（0 <= <number> <= {config.guessnum.max}）")
        else:
            await commands.guessnum.finish("游戏已存在")
    # Ranking
    elif argv[0] == "list":
        await commands.guessnum.finish("敬请期待")
    # Stop Game
    # elif argv[0] == "stop":
    #    try:
    #        answer = config.guessnum.number.pop(group)
    #    except KeyError:
    #        await commands.guessnum.finish("找不到游戏", at_sender=True)
    #    else:
    #        await commands.guessnum.finish(f"游戏结束，正确答案：{answer}")
    else:
        # Guess number
        try:
            guessed = int(argv[0])
            if guessed == config.guessnum.number[group]:
                # Add coin
                coin = __mysql__.add_coin_for_user(
                    int(event.get_user_id()), random.randint(0, 10))[1]
                level_update_data = __mysql__.add_exp_for_user(
                    int(event.get_user_id()), 2)

                # Finish
                answer = config.guessnum.number.pop(group)
                await commands.guessnum.finish(f"{answer}，回答正确！", at_sender=True)
            elif guessed > config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，大了", at_sender=True)
            elif guessed < config.guessnum.number[group]:
                await commands.guessnum.finish(f"{guessed}，小了", at_sender=True)
        except KeyError:
            await commands.guessnum.finish(f"游戏未开始或已结束，使用 {config.__config__.command_help.command_start}guess start 创建游戏", at_sender=True)
        except ValueError:
            await commands.guessnum.finish(f"""未知参数：{argv[0]}
/guess start （开始游戏）
/guess <number: int> （作答）
/guess list（排行榜：敬请期待）
在游戏进行中：<number: int>（作答）""".replace("/", config.__config__.command_help.command_start))
