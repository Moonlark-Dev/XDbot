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
            email_subject = argv.split("\n")[1]
            email_message = ""
            for msg in argv.split("\n")[2:]:
                email_message += msg + "\n"
            # 解析信息
            sending_message = f"""From: {config.email.smtp_user}
Subject: {email_subject}

{email_message}

----------------------
发件人：{event.sender.card}({event.get_user_id()})""".encode("utf-8")
            logger.info(
                f"Sending {sending_message} to {to_addrs} (use {config.email.smtp_user})")
            # 发送邮件
            try:
                smtp = smtplib.SMTP(config.email.smtp_server_host,
                                    config.email.smtp_server_port)
                smtp.connect(config.email.smtp_server_host,
                             config.email.smtp_server_port)
                smtp.login(config.email.smtp_user, config.email.smtp_passwd)
                smtp.auth_login()
                smtp.sendmail(
                    from_addr=config.email.smtp_user,
                    to_addrs=to_addrs,
                    msg=sending_message
                )
                smtp.quit()
            except Exception as e:
                logger.error("Error to send email: {e}")
                return await commands.send_email.finish(f"发送失败\n{e}", at_sender=True)
            logger.success("Email sent!")
            config.email.latest_send = time.time()
            await commands.send_email.finish("邮件已发送", at_sender=True)
        else:
            await commands.send_email.finish("冷却中！", at_sender=True)
