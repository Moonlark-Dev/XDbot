# Import libraries
from sys import path
import os.path
from nonebot.log import logger
import nonebot.adapters.onebot.v11
import nonebot.params
import json
import asyncio

# Read plugins config
config = json.load(open("./data/XDbot/plugins.json"))
if "search" not in config.keys():
    config["search"] = {"disabled": []}

# Submodules
submodules_list = ["bdwiki", "bing"]
submodules = {}

# Import modules
logger.info("Search: Loading submodules . . .")
logger.info("=" * 30)

path.append(os.path.dirname(os.path.abspath(__file__)))
for module in submodules_list:
    if module not in config["search"]["disabled"]:
        try:
            submodules[module] = __import__(f"{module}")
            # f"src.plugins.Core.search.{module}")
            # logger.info(f"src.plugins.Core.search.{module}")
            # logger.warning(dir(submodules[module]))
            logger.success(f"Loaded submodule {module}")
        except Exception as e:
            logger.error(f"Cannot load submodule {module}: {e}")
    else:
        logger.warning(f"Submodule {module} has been disabled.")
logger.success(
    f"Loaded {submodules.keys().__len__()}/{submodules_list.__len__()} submodules."
)

# Command
search = nonebot.on_command("search")
cache = {}


class searchTools():

    def __init__(self, name):
        self.name = name

    async def finish(self, res):
        await search.send(f"来自{self.name}的搜索结果：\n{res}")

    def add_page(self, name, data):
        global cache
        cache[name] = data


@search.handle()
async def get_search(message: nonebot.adapters.onebot.v11.Message = nonebot.
                     params.CommandArg()):
    msg = message.extract_plain_text()
    arg = msg.split(" ")
    #answer = ""
    if arg[0] == "list":
        await search.finish(f"已经加载的子模块：{list(submodules.keys())}")
    elif arg[0] == "view":
        try:
            answer = cache[arg[1]]
        except KeyError:
            answer = "页面不存在"
        await search.finish(nonebot.adapters.onebot.v11.Message(answer))
    elif arg[0] in submodules.keys():
        keyword = msg[len(arg[0]):]
        await search.send(f"正在{arg[0]}上搜索「{keyword}」")
        asyncio.create_task(submodules[arg[0]].search(keyword=keyword,
                                       tool=searchTools(arg[0])))
    else:
        await search.send(f"正在{len(submodules.keys())}个引擎中搜索「{msg}」")
        logger.info(submodules)
        for submodule in submodules.keys():
            logger.info(dir(submodules[submodule]))
            asyncio.create_task(submodules[submodule].search(
                keyword=msg, tool=searchTools(submodule)))


logger.info("=" * 30)
logger.info("Search: Initialization complete!")
