from . import __commands__ as commands
import nonebot.adapters.onebot.v11.bot
import nonebot.adapters.onebot.v11
import nonebot.params

@commands.notice.handle()
async def notice_handle(
    bot: nonebot.adapters.onebot.v11.bot.Bot,
    args: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    for i in await bot.get_group_list():
        await bot.send_group_msg(
            group_id=i['group_id'],
            message=nonebot.adapters.onebot.v11.Message('【超级广播】\n' + args)
        )
