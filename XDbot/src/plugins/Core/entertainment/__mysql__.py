from . import __config__ as config
from nonebot.log import logger
import pymysql


def connect():
    database = pymysql.connect(
        host=config.mysql.host,
        user=config.mysql.user,
        passwd=config.mysql.passwd,
        database=config.mysql.database
    )
    cursor = database.cursor()
    return database, cursor


def get_user_data(id, item):
    """
    get_user_data(id: int, item: int) -> Any
    Item: 
        [0] ID, [1] Level, [2] EXP, [3] Coin, [4] Chicked-In
    """
    database, cursor = connect()
    try:
        cursor.execute(f"""SELECT * FROM {config.mysql.table['users']} \
                WHERE id={id}""")
        result = cursor.fetchall()
        # database.close()
        return result[0][item]
    except IndexError:
        cursor.execute(f"""INSERT INTO {config.mysql.table['users']} (id) \
                VALUES ({id})""")
        database.commit()
        database.close()
        return get_user_data(id, item)

    except Exception as e:
        database.close()
        logger.error(str(e))


def set_user_data(id, item, value):
    database, cursor = connect()
    try:
        cursor.execute(
            f"UPDATE {config.mysql.table['users']} set {item}={value} WHERE id={id}")
        database.commit()
    except Exception as e:
        logger.error(str(e))
    database.close()


def add_coin_for_user(id, number):
    coin = get_user_data(id, 3) + number
    set_user_data(id, "coin", coin)
    logger.info(
        f"User {id} now has {coin}(+{number}) {config.currency_symbol}")
    return id, number, coin


def add_exp_for_user(id, number):
    exp = get_user_data(id, 2) + number
    level = get_user_data(id, 1)
    if exp >= level**2:
        exp -= level ** 2
        level += 1
        level_update = True
    else:
        level_update = False
    set_user_data(id, "experience", exp)
    set_user_data(id, "level", level)
    return level_update, exp, level
