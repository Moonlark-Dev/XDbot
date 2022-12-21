import requests
#import json


class get_center():

    def get(text, start, end, find_start=0):
        text_start = text.find(start, find_start) + start.__len__()
        text_end = text.find(end, text_start)
        return text[text_start:text_end]


def get_list(list_text, start=0):
    if list_text.find('<div class="b_title">', start) != -1:
        return [
            get_center.get(list_text, '<h2>', "</h2>",
                           list_text.find('<div class="b_title">', start))
        ] + get_list(list_text,
                     list_text.find('<div class="b_title">', start) + 15)
    else:
        return []


def get_url(html):
    url = get_center.get(html, "href=\"", '"')
    title = get_center.get(html, ">", "</a>")
    title = title.replace("<strong>", "")
    title = title.replace("</strong>", "")
    return [title, url]


def bing(keyword, page="1"):
    req = requests.get("https://cn.bing.com/search?q=" + keyword + "&first=" +
                       page)
    html = req.text
    list_text = get_center.get(html, '<ol id="b_results" class="">', "</ol>")
    html_list = get_list(list_text)

    search_list = []
    for h in html_list:
        search_list += [get_url(h)]

    text = ""
    length = 0
    for s in search_list:
        length += 1
        text += f"{length}. {s[0]} （{s[1]}）\n"

    return text
    # print(search_list)


#search = on_command("search")


#@search.handle()
async def search(keyword, tool):
    args = keyword
    answer = ""

    # 检查关键词
    if args == "":
        await search.finish(message=Message("请输入搜索关键词"), at_sender=True)
    else:
        answer += bing(args)
        await tool.finish(answer)
