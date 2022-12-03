import nonebot

guessnum_onmsg = nonebot.on_message()
sign_command = nonebot.on_command("sign", aliases={"签到"})
sign_keyword = nonebot.on_keyword({"签到"})
guessnum = nonebot.on_command("guess", aliases={"gn"})
