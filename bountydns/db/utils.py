from bountydns.core.utils import getenv


def make_db_url(key):
    DB_DRIVER = getenv(key.upper() + "_" + "DB_DRIVER")
    DB_SERVER = getenv(key.upper() + "_" + "DB_HOST")
    DB_USER = getenv(key.upper() + "_" + "DB_USER")
    DB_PASSWORD = getenv(key.upper() + "_" + "DB_PASSWORD")
    DB_DATABASE = getenv(key.upper() + "_" + "DB_DATABASE")
    SQLALCHEMY_DATABASE_URI = (
        f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"
    )
    return SQLALCHEMY_DATABASE_URI
