import nonebot
import nonebot.adapters.onebot.v11.message
import nonebot.adapters.onebot.v11

st = nonebot.on_command("st")


@st.handle()
async def _():
    try:
        await st.finish(
            nonebot.adapters.onebot.v11.message.Message(
                nonebot.adapters.onebot.v11.MessageSegment.image(
                    "https://www.dmoe.cc/random.php")))
    except:
        pass
