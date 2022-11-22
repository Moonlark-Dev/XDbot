from . import __config__ as config
from . import __commands__ as commands
import pymysql


def connect_database():
    return pymysql.connect(
            host=config.cave.host,
            user=config.cave.user,
            password=config.cave.password,
            database=config.cave.database
        )


@commands.cave.handle()
async def cave_handle():
    database = connect_database()
    cursor = database.cursor()
    data = cursor.execute(config.cave.get_all_id)
