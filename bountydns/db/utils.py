from bountydns.core.utils import getenv


def make_db_url():
    DB_DRIVER = getenv("DB_DRIVER", "postgresql")
    if "sqlite" in DB_DRIVER:
        DB_DATABASE = getenv("DB_DATABASE", "", optional=True)
        SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}:///{DB_DATABASE}"
    else:
        DB_DATABASE = getenv("DB_DATABASE", "postgres")
        DB_SERVER = getenv("DB_HOST", "db")
        DB_USER = getenv("DB_USER", "postgres")
        DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
        DB_PORT = getenv("DB_PORT", "5432")
        SQLALCHEMY_DATABASE_URI = (
            f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_DATABASE}"
        )

    return SQLALCHEMY_DATABASE_URI
