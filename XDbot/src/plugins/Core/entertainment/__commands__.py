import nonebot

guessnum_onmsg = nonebot.on_message()
guessnum = nonebot.on_command("guess", aliases = {"gn"})
