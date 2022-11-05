from . import __config__ as config
from . import __commands__ as commands
import nonebot
import nonebot.adapters.onebot.v11.bot
import nonebot.adapters.onebot.v11.event
import nonebot.adapters.onebot.v11
import nonebot.params
import nonebot.permission
import json
import os.path


@commands.helplist.handle()
async def help_handle(
        args: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    # Read command list
    command_list = json.load(
        open(
            os.path.join(
                os.path.abspath("."),
                "data/help/commands.json"
            ),
            encoding="utf-8"
        )
    )
    if str(args) == "":
        # Command List
        # TODO 多页面支持
        commands = f"指令列表 —— {config.bot_nickname}\n"
        for command in command_list.keys():
            command_data = command_list[command]
            if command_data["enable"]:
                commands += f"[√] {command_data['name']}: {command_data['info']}\n"
        commands += config.command_help.list_backhander
        await commands.helplist.finish(commands)
    else:
        try:
            command = command_list[args.extract_plain_text()]
        except KeyError as e:
            return await commands.helplist.finish(f"未知指令：{e}")
        # Parsing command
        answer = f"""
说明：{command['msg']}
用法（{len(command['usage'])}）："""
        length = 1
        for usage in command["usage"]:
            answer += f"\n{length}. {config.command_help.command_start}{usage}\n"
            length += 1
        if not command["enable"]:
            answer += "\n警告：指令被标记为不可用"
        await commands.helplist.finish(answer, at_sender=True)

# TODO 移动到 Admin 插件中
"""
helpadmin = on_command("help-set", permission = SUPERUSER)
@helpadmin.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    r = str(args).split("\n")
    if r[0] == "init":
        try: os.mkdir("data")
        except: pass

        try: os.mkdir("./data/help")
        except: pass

        json.dump({}, open("./data/help/commands.json", "w", encoding = "utf-8"))

        await helpadmin.finish("完成")
    
    elif r[0] == "edit":
        command_list = json.load(open("./data/help/commands.json", encoding = "utf-8"))
        
        if   r[3] == "True":  r[3] = True
        elif r[3] == "False": r[3] = False

        command_list[r[1]][r[2]] = r[3]
        json.dump(command_list, open("./data/help/commands.json", "w", encoding = "utf-8"))

        await helpadmin.finish("完成")

    elif r[0] == "add":
        command_list = json.load(open("./data/help/commands.json", encoding = "utf-8"))
        
        if   r[3] == "True":  r[3] = True
        elif r[3] == "False": r[3] = False
        
        command           = {}
        command["name"]   = r[1]
        command["info"]   = r[2]
        command["msg"]    = r[3]
        command["usage"]  = r[4].replace("&#91;\\n&#93;", "\n")
        command["enable"] = True

        command_list[r[1]] = command
        json.dump(command_list, open("./data/help/commands.json", "w", encoding = "utf-8"))

        await helpadmin.finish("完成")
"""
