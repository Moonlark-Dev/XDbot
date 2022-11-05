from . import __commands__ as commands
import psutil
import os.path
import getpass


async def get_status():
    # CPU
    # _cpu = psutil.cpu_percent(interval=1, percpu=True)
    _cpu = psutil.cpu_percent(1, True)
    cpu = [0, 0]
    for c in _cpu:
        cpu[0] += c
    cpu[1] = _cpu.__len__() * 100
    # Memory
    _mem = psutil.virtual_memory()
    mem = [
        int(_mem.used / 1024 / 1024 / 1024 * 100) / 100,
        int(_mem.total / 1024 / 1024 / 1024 * 100) / 100
    ]
    mem_percent = _mem.percent
    # Swap
    _swp = psutil.swap_memory()
    swp = [
        int(_swp.used / 1024 / 1024 / 1024 * 100) / 100,
        int(_swp.total / 1024 / 1024 / 1024 * 100) / 100
    ]
    # Return
    return f"""运行状态：
处理器：{cpu[0]} / {cpu[1]}%
运行内存：{mem[0]} / {mem[1]}GB ({mem_percent}%)
虚拟内存：{swp[0]} / {swp[1]}GB
系统类型：{os.name}
登录用户：{getpass.getuser()}"""


@commands.status.handle()
async def status_handle():
    await commands.status.finish(await get_status())
