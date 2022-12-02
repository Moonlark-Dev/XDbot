from . import __config__ as config
from . import __commands__ as commands
import nonebot.adapters.onebot.v11
import nonebot.params
import os.path
from playwright.async_api import async_playwright
import asyncio
from nonebot.log import logger


async def test_playwright_available():
    """Test if Playwright is available"""
    logger.info("Testing whether Playwright is available . . .")
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        await browser.close()
    logger.success("Playwright is available!")


@commands.preview.handle()
async def preview_handle(
    url: nonebot.adapters.onebot.v11.Message = nonebot.params.CommandArg()
):
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(str(url))
        await page.screenshot(path="./data/preview.png", full_page=True)
        await browser.close()
    await commands.preview.finish(
        nonebot.adapters.onebot.v11.Message(
            nonebot.adapters.onebot.v11.MessageSegment.image(
                f"file:///{os.path.abspath('./data/preview.png')}"
            )
        )
    )


if config.preview.test_playwright:
    asyncio.run(test_playwright_available())
