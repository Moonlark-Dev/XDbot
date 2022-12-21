# Import libraries
from nonebot.log import logger
import os
import os.path
import json
import asyncio

# Check files
logger.info("Checking files in files.json")
path = os.path.dirname(os.path.abspath(__file__))
files = json.load(open(os.path.join(path, "files.json")))
for file in files:
    if file["is_dir"]:
        logger.info(f"Checking directory: {file['path']} . . .")
        if not os.path.isdir(file["path"]):
            os.mkdir(file["path"])
    else:
        logger.info(f"Checking file: {file['path']}")
        if not os.path.isfile(file["path"]):
            if file["default"]["file"]:
                # Copy file
                with open(file["default"]["path"].replace("${PluginDir}", path),
                          mode="rb") as f1:
                    with open(file["path"], "wb") as f2:
                        f2.write(f1.read())
            else:
                with open(file["path"], "w", encoding="utf-8") as f:
                    f.write(file["default"]["text"])

# Read plugins config
config = json.load(open("./data/XDbot/plugins.json"))

# Modules
modules = [
    "reboot",
    "messenger",
    "search",
    "system",
    "status",
    "geturl",
    "notice",
    "code",
    #   "whoat",
    "st",
    "screenshot",
    #    "report_error",
    "jrrp",
    "execute",
    "about",
    "help",
    "fanyi",
    "ping",
    "email",
    "preview",
    "reply",
    "entertainment",
]
plugin_modules = {}

# Import modules
for module in modules:
    if module not in config["disabled"]:
        try:
            plugin_modules[module] = __import__(f"src.plugins.Core.{module}")
            # logger.warning(dir(plugin_modules[module]))
            logger.success(f"Loaded module {module}")
        except Exception as e:
            logger.error(f"Cannot load module {module}: {e}")
    else:
        logger.warning(f"Module {module} has been disabled.")
logger.success(
    f"Loaded {plugin_modules.keys().__len__()}/{modules.__len__()} plugins.")

# Create help file
help_json = json.load(
    open(os.path.join(path, "commands.json"), encoding="utf-8"))
loaded_plugins = plugin_modules.keys()
for command in help_json.keys():
    if help_json[command]["module"] in loaded_plugins:
        help_json[command]["enable"] = True
    else:
        help_json[command]["enable"] = False
json.dump(help_json, open(
    "./data/XDbot/help/commands.json", "w", encoding="utf-8"))
logger.success("Help file created.")

logger.info("Initialization complete!")
