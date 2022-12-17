import json
from . import __config__ as config
from . import __mysql__
from nonebot.log import logger


def get_items():
    database, cursor = __mysql__.connect()
    cursor.execute(f"""SELECT * FROM {config.mysql.table['items']}""")
    result = cursor.fetchall()
    database.close()
    return result


def get_item(id):
    return get_items()[id]


def get_user_bag(id):
    bags = json.load(open("./data/XDbot/bags/bags.json"))
    if id not in bags:
        bags[id] = []
        json.dump(bags, open("./data/XDbot/bags/bags.json", "w"))
    return bags[id]


def user_get_item(id, item_id, item_count, item_data={}):
    if item_id == 7:
        # VimCoin
        __mysql__.add_coin_for_user(id, item_count)
        return False
    elif item_id == 8:
        # EXP
        __mysql__.add_exp_for_user(id, item_count)
        return False
    else:
        return True


# def use_item(id, item_id, item_count, item_data):
#    if item_id ==


def give_user_item(id, item_id, item_count, item_data={}):
    bags = get_user_bag(id)
    user_has_item = False
    length = 0
    for item in bags:
        if item["id"] == id and item["data"] == item_data:
            user_has_item = True
            break
        length += 1
    if user_get_item(id, item_id, item_count, item_data):
        if user_has_item:
            bags[length]["count"] += 1
        else:
            bags += [
                {
                    "id": item_id,
                    "count": item_count,
                    "data": item_data
                }
            ]
        logger.info(f"Gave {item_id}({item_data}) *{item_count} to {id}")
