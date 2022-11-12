#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import os

system=on_command("system", aliases={"run", "执行", "执行系统指令"}, permission=SUPERUSER)

@system.handle()
async def system_handle(event: MessageEvent, args: Message = CommandArg()):
    cm=args.extract_plain_text()
    run_req=os.popen(cm)
    run_req=run_req.read()
    await system.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("".join(run_req)))

