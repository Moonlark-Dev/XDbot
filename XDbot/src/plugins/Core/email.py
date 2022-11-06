from . import __commands__ as commands
from . import __config__ as config
from nonebot.log import logger
import nonebot.adapters.onebot.v11.event
import nonebot.adapters.onebot.v11
import nonebot.params
import time
import smtplib


@commands.send_email.handle()
async def sendemail_handle(
    event: nonebot.adapters.onebot.v11.event.MessageEvent,
    message: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    if time.time() - config.email.latest_send >= config.email.send_sleep:
        argv = str(message)
        if argv != "":
            # 获取信息
            to_addrs = argv.split("\n")[0].split(" ")
            subject = argv.split("\n")[1]
            message = ""
            for msg in argv.split("\n")[2:]:
                message += msg + "\n"
            # 解析信息
            msg = f"""From: {config.email.smtp_user}
Subject: {subject}

{message}

----------------------
发件人：{event.sender.card}({event.get_user_id()})""".encode("utf-8")
            logger.info(f"Message: {msg}")
            logger.info(f"To: {to_addrs}")
            # 发送邮件
            smtp = smtplib.SMTP(config.email.smtp_server)
            smtp.login(config.email.smtp_user, config.email.smtp_passwd)
            smtp.auth_login()
            smtp.sendmail(
                from_addr=config.email.smtp_user,
                to_addrs=to_addrs,
                msg=msg
            )
            smtp.quit()
            config.email.latest_send = time.time()
            await commands.send_email.finish("邮件已发送", at_sender=True)
        else:
            await commands.send_email.finish("冷却中！", at_sender=True)
