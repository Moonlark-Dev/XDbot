#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nonebot

st = nonebot.on_command("st")
translate = nonebot.on_command("translate", aliases={"fanyi", "tn"})
jrrp = nonebot.on_command("jrrp")
preview = nonebot.on_command("preview")
about = nonebot.on_command("about")
ping = nonebot.on_command("ping")
status = nonebot.on_command("status")
ping_full_log = nonebot.on_command("ping-f")
helplist = nonebot.on_command("help")
send_email = nonebot.on_command("send-email")
