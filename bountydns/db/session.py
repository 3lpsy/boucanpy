from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

dbs = {}


def session(key):
    return dbs[key]["Session"]()


def db_session(key):
    return dbs[key]["db_session"]


def engine(key):
    return dbs[key]["engine"]


def db_url(key):
    return dbs[key]["url"]


def metadata(key):
    return dbs[key]["metadata"]


def db_register(key, db_uri):
    global dbs
    engine = create_engine(db_uri)
    dbs[key] = {
        "engine": engine,
        "Session": sessionmaker(autocommit=False, autoflush=False, bind=engine),
        "db_session": scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        ),
        "url": db_uri,
        "metadata": getattr(
            import_module(f"bountydns.db.{key}.models.base", "base"), "metadata"
        ),
        "models": getattr(
            import_module(f"bountydns.db.{key}.models", "models"), "models"
        ),
    }
