from . import __commands__ as command
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11


@command.st.handle()
async def st_handle():
    try:
        await command.st.finish(
            nonebot.adapters.onebot.v11.message.Message(
                nonebot.adapters.onebot.v11.MessageSegment.image(
                    "https://www.dmoe.cc/random.php")))
    except Exception:
        pass
