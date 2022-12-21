#from nonebot.adapters.onebot.v11.message import MessageSegment
# from nonebot.log import logger
import requests
import json


async def search(keyword, tool):
    req = requests.get(
        f"http://api.muxiaoguo.cn/api/Baike?type=Baidu&word={keyword}&api_key=a9f05a26ee2778e2"
    )
    data = json.loads(req.text)
    answer = ""

    if data["code"] == 200:
        answer += data["data"]["content"]
    #    answer += MessageSegment.image(data["data"]["ImgUrl"])
    else:
        answer += f"查找失败（{data['code']}）：{data['msg']}"

    await tool.finish(answer)
