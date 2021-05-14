from motor.motor_asyncio import AsyncIOMotorClient
from .utils import load_config
from fastapi_mail import ConnectionConfig

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


############### MONGO BACKUP DATABASE ####################


BACKUP_DB_CLIENT = AsyncIOMotorClient(
    host=CONF.get("databases")["backup"]["HOST"],
    port=int(CONF.get("databases")["backup"]["PORT"]),
    username=CONF.get("databases")["backup"]["USER"],
    password=CONF.get("databases")["backup"]["PASSWORD"],
)

BACK_UP_DB = BACKUP_DB_CLIENT[CONF.get("databases")["backup"]["NAME"]]


def close_backup_db_client():
    BACKUP_DB_CLIENT.close()




############# Email conf ##################
EMAIL_CONF = ConnectionConfig(
        MAIL_USERNAME = CONF.get("mail")["MAIL_USERNAME"],
        MAIL_PASSWORD = CONF.get("mail")["MAIL_PASSWORD"],
        MAIL_FROM = CONF.get("mail")["MAIL_FROM"],
        MAIL_FROM_NAME = CONF.get("mail")["MAIL_FROM_NAME"],
        MAIL_PORT = CONF.get("mail")["MAIL_PORT"],
        MAIL_SERVER = CONF.get("mail")["MAIL_SERVER"],
        MAIL_TLS = CONF.get("mail")["MAIL_TLS"] ,
        MAIL_SSL = CONF.get("mail")["MAIL_SSL"]
)
