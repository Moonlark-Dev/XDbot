#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import modules
from . import status
from . import st

# Import libraries
from nonebot.log import logger
import os
import os.path
import json

# Check files
path = os.path.dirname(os.path.abspath(__file__))
files = json.load(open(os.path.join(path, "init.json")))
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
                        mode="rb", encoding="utf-8") as f1:
                    with open(file["default"]["path"], "wb",
                            encoding="utf-8") as f2:
                        f2.write(f1.read())
            else:
                with open(file["path"], "w", encoding="utf-8") as f:
                    f.write(file["default"])
logger.info("Done")
