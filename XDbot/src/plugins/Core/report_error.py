import nonebot
import traceback


def debug(func):
    @wraps
    def decorator():
        try:
            func()
        except:
            e = traceback.format_exc()
            bot = nonebot.get_bot()
            for i in nonebot.get_driver().config.superusers:
                bot.send(user_id=i, message=f"{e}")
    return decorator
