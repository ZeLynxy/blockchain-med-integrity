from motor.motor_asyncio import AsyncIOMotorClient
from .utils import load_config


CONF = load_config()

############### MONGO DATABASE ####################

DB_CLIENT = AsyncIOMotorClient(
    host=CONF.get("databases")["default"]["HOST"],
    port=int(CONF.get("databases")["default"]["PORT"]),
    username=CONF.get("databases")["default"]["USER"],
    password=CONF.get("databases")["default"]["PASSWORD"],
)

DB = DB_CLIENT[CONF.get("databases")["default"]["NAME"]]

def close_db_client():
    DB_CLIENT.close()

