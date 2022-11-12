from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg

TellAll = on_command("broadcast", aliases = {"notice"}, permission = SUPERUSER)
@TellAll.handle()
async def _(bot: Bot,event: GroupMessageEvent,args: Message = CommandArg()):
    # if not await SUPERUSER(bot, event):
        # await TellAll.finish("Permission denied!")

    for i in await bot.get_group_list():
        await bot.send_group_msg(group_id = i['group_id'], message = Message('【超级广播】\n' + args))
    await TellAll.finish(f"已成功在 {bot.get_group_list().__len__()} 个群广播信息")
