# Import libraries
from nonebot.log import logger
import json

# Read plugins config
config = json.load(open("./data/XDbot/plugins.json"))
if "entertainment" not in config.keys():
    config["entertainment"] = {"disabled": []}

# Submodules
submodules = [
    "guessnum",
    "sign",
    "hijack",
    "user"
]
plugin_modules = {}

# Import modules
logger.info("Entertainment: Loading submodules . . .")
logger.info("="*30)

for module in submodules:
    if module not in config["entertainment"]["disabled"]:
        try:
            plugin_modules[module] = __import__(
                f"src.plugins.Core.entertainment.{module}")
            # logger.warning(dir(plugin_modules[module]))
            logger.success(f"Loaded submodule {module}")
        except Exception as e:
            logger.error(f"Cannot load submodule {module}: {e}")
    else:
        logger.warning(f"Submodule {module} has been disabled.")
logger.success(
    f"Loaded {plugin_modules.keys().__len__()}/{submodules.__len__()} submodules.")


logger.info("="*30)
logger.info("Entertainment: Initialization complete!")
