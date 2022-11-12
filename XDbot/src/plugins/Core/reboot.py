from . import __commands__ as commands
import random


@commands.reboot.handle()
async def reboot_handle():
    with open("./data/reboot.py", "w") as f:
        f.write(f"print({random.randint(0, 100)})")
