#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import Arg, CommandArg, ArgPlainText

import random

reboot=on_command("reboot", permission=SUPERUSER)

@reboot.handle()
async def _(event: MessageEvent):
    with open("./data/reboot.py", "w") as f:
        f.write(f"print({random.randint(0, 100)})")


