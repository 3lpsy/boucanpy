from os.path import join, exists
from bountydns.core.utils import getenv, storage_dir


def resolve_db_path(db_path):
    if db_path:
        # if a full path is passed & db file exists, allow it
        if not exists(db_path):
            db_path = storage_dir(join("database", db_path))
    return db_path


def get_resolved_db_path():
    DB_DATABASE = getenv("DB_DATABASE", "", optional=True)  # null for in memory db
    return resolve_db_path(DB_DATABASE)


def make_db_url():
    DB_DRIVER = getenv("DB_DRIVER", "postgresql")
    if "sqlite" in DB_DRIVER:
        DB_DATABASE = get_resolved_db_path()
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
