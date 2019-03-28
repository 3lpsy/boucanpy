from bountydns.core.utils import getenv


def make_db_url():
    DB_DRIVER = getenv("DB_DRIVER")
    DB_DATABASE = getenv("DB_DATABASE")
    if "sqlite" in DB_DRIVER:
        SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}:///{DB_DATABASE}"
    else:
        DB_SERVER = getenv("DB_HOST")
        DB_USER = getenv("DB_USER")
        DB_PASSWORD = getenv("DB_PASSWORD")
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"
        )

    return SQLALCHEMY_DATABASE_URI
