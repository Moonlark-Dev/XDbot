import json
from . import __config__ as config
from . import __mysql__
from nonebot.log import logger
import random


def get_items():
    database, cursor = __mysql__.connect()
    cursor.execute(f"""SELECT * FROM {config.mysql.table['items']}""")
    result = cursor.fetchall()
    database.close()
    return result


def get_item(item_id):
    return get_items()[item_id]


def get_user_bag(user_id):
    bags = json.load(open("./data/XDbot/bags/bags.json"))
    if user_id not in bags:
        bags[user_id] = []
        json.dump(bags, open("./data/XDbot/bags/bags.json", "w"))
    return bags[user_id]


def save_user_bag(user_id, bag):
    bags = json.load(open("./data/XDbot/bags/bags.json"))
    bags[user_id] = bag
    json.dump(bags, open("./data/XDbot/bags/bags.json", "w"))
    # return bags[user_id]


def user_get_item(user_id, item_id, item_count, item_data={}):
    if item_id == 7:
        # VimCoin
        __mysql__.add_coin_for_user(user_id, item_count)
        return False
    elif item_id == 8:
        # EXP
        __mysql__.add_exp_for_user(user_id, item_count)
        return False
    else:
        return True


# def use_item(id, item_id, item_count, item_data):
#    if item_id ==


def give_user_item(user_id, item_id, item_count, item_data={}):
    bag = get_user_bag(user_id)
    logger.info(bag)
    user_has_item = False
    length = 0
    for item in bag:
        if item["id"] == item_id and item["data"] == item_data:
            user_has_item = True
            break
        length += 1
    if user_get_item(user_id, item_id, item_count, item_data):
        if user_has_item:
            bag[length]["count"] += item_count
            if bag[length]["count"] == 0:
                bag.pop(length)
                logger.info(
                    f"Gave {item_id}({item_data}) *{item_count} to {user_id}")
                save_user_bag(user_id, bag)
                return True
            elif bag[length]["count"] < 0:
                # bag[length]["count"] -= item_count
                logger.warning(
                    f"Cannot give {item_id}({item_data}) *{item_count} to {user_id}: User doesn't have enough items")
                return False
            else:
                logger.info(
                    f"Gave {item_id}({item_data}) *{item_count} to {user_id}")
                save_user_bag(user_id, bag)
                return True
        elif item_count < 0:
            logger.warning(
                f"Cannot give {item_id}({item_data}) *{item_count} to {user_id}: User doesn't have items")
            return False
        else:
            bag += [
                {
                    "id": item_id,
                    "count": item_count,
                    "data": item_data
                }
            ]
            logger.info(f"Gave {item_id}({item_data}) *{item_count} to {user_id}")
            save_user_bag(user_id, bag)
            return True
    else:
        logger.info(f"Gave {item_id}({item_data}) *{item_count} to {user_id}")
        # save_user_bag(user_id, bag)
        return True
    


def user_use_item(user_id, item_id, item_data={}):
    # 每日 VimCoin 礼包
    if item_id == 0:
        if random.random() <= 0.15:
            if random.random() <= 0.20:
                count = random.randint(0, 50)
            elif random.random() <= 0.10:
                count = random.randint(25, 50)
            else:
                count = random.randint(0, 25)
        else:
            count = int(random.random()*7.1*random.random()*7.1)
        give_user_item(user_id, 7, count)
        return f"每日礼包：你获得了{count} {config.currency_symbol}"
    # 每日 EXP 礼包
    elif item_id == 1:
        count = random.randint(0, 30)
        give_user_item(user_id, 8, count)
        return f"每日礼包：你获得{count} EXP"
    # VimCoin 礼包
    elif item_id == 9:
        count = random.randint(20, 100)
        give_user_item(user_id, 8, count)
        return f"你获得了{count} {config.currency_symbol}"


def use_item(user_id, item_pos, count):
    bag = get_user_bag(user_id)
    item = bag[item_pos]
    if give_user_item(user_id, item["id"], -1, item["data"]):
        r = user_use_item(user_id, item["id"], item["data"])
        if count > 1:
            return use_item(user_id, item_pos, count - 1) + [r]
        else:
            return [r]
    else:
        return ["114514"]
