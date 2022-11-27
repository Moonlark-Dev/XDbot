import nonebot
import nonebot.permission
import nonebot.rule

to_me = nonebot.on_message(rule=nonebot.rule.to_me())
st = nonebot.on_command("st")
cave = nonebot.on_command("cave")
translate = nonebot.on_command("translate", aliases={"fanyi", "tn"})
jrrp = nonebot.on_command("jrrp")
preview = nonebot.on_command("preview")
messenger = nonebot.on_command("messenger", aliases={"信使", "msg"})
messenger_sender = nonebot.on_message()
about = nonebot.on_command("about")
code = nonebot.on_command("code")
notice = nonebot.on_command("broadcast", aliases = {"notice"}, permission = nonebot.permission.SUPERUSER)
ping = nonebot.on_command("ping")
status = nonebot.on_command("status")
screenshot = nonebot.on_command("screenshot")
geturl = nonebot.on_command("get")
ping_full_log = nonebot.on_command("ping-f")
random_send_pic = nonebot.on_message()
random_save_pic = nonebot.on_message()
helplist = nonebot.on_command("help")
reboot=nonebot.on_command("reboot", permission=nonebot.permission.SUPERUSER)
send_email = nonebot.on_command("send-email")
echo = nonebot.on_command("echo", permission=nonebot.permission.SUPERUSER)
execute = nonebot.on_command(
    "execute", permission=nonebot.permission.SUPERUSER)
system = nonebot.on_command("system", aliases={
                            "run", "执行", "执行系统指令"}, permission=nonebot.permission.SUPERUSER)
