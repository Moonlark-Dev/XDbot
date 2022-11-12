import nonebot
import nonebot.permission

st = nonebot.on_command("st")
translate = nonebot.on_command("translate", aliases={"fanyi", "tn"})
jrrp = nonebot.on_command("jrrp")
preview = nonebot.on_command("preview")
messenger = nonebot.on_command("messenger", aliases={"信使", "msg"})
messenger_sender = nonebot.on_message()
about = nonebot.on_command("about")
ping = nonebot.on_command("ping")
status = nonebot.on_command("status")
ping_full_log = nonebot.on_command("ping-f")
helplist = nonebot.on_command("help")
send_email = nonebot.on_command("send-email")
echo = nonebot.on_command("echo", permission=nonebot.permission.SUPERUSER)
helpadmin = nonebot.on_command(
    "help-set", permission=nonebot.permission.SUPERUSER)
execute = nonebot.on_command(
    "execute", permission=nonebot.permission.SUPERUSER)
system = nonebot.on_command("system", aliases={
                            "run", "执行", "执行系统指令"}, permission=nonebot.permission.SUPERUSER)
