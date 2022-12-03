from . import __commands__ as commands
from . import __config__ as config
from . import __mysql__
import nonebot.adapters.onebot.v11.event
import nonebot.adapters.onebot.v11
import nonebot.params


@commands.user_status.handle()
async def user_status_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent
):
    print(114514*2)
    qq = int(event.get_user_id())
    user = {
        "id": __mysql__.get_user_data(qq, 0),
        "level": __mysql__.get_user_data(qq, 1),
        "exp": __mysql__.get_user_data(qq, 2),
        "coins": __mysql__.get_user_data(qq, 3)
    }
    await commands.user_status.finish(f"""「用户信息」
ID：{user["id"]}
等级：{user["level"]} [{int(user["exp"]/user["level"]**2*10)*"="}{int(10-(user["exp"]/user["level"]**2*10))*" "}] ({user["exp"]}/{user["level"]**2})
{config.currency_name}：{user["coins"]}{config.currency_symbol}""")
