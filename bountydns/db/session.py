from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from bountydns.db.paginate.query import PaginationQuery

DEFAULT_KEY = "api"

dbs = {}
_sessions = {}

# TODO: fix this, move back to single database target
def session(key=None):
    key = key or DEFAULT_KEY
    if key in _sessions.keys():
        return _sessions[key]
    session = dbs[key]["Session"]()
    _sessions[key] = session
    return session


def db_session(key=None):
    key = key or DEFAULT_KEY
    return dbs[key]["db_session"]


def engine(key=None):
    key = key or DEFAULT_KEY
    return dbs[key]["engine"]


def db_url(key=None):
    key = key or DEFAULT_KEY
    return dbs[key]["url"]


def metadata(key=None):
    key = key or DEFAULT_KEY
    return dbs[key]["metadata"]


def db_register(key, db_uri):
    global dbs
    engine = create_engine(db_uri)
    db = {}
    db["engine"] = engine
    db["Session"] = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, query_cls=PaginationQuery
    )
    db["db_session"] = scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False, bind=engine, query_cls=PaginationQuery
        )
    )
    db["url"] = db_uri
    db["metadata"] = getattr(
        import_module(f"bountydns.db.models.base", "base"), "metadata"
    )
    db["models"] = getattr(import_module(f"bountydns.db.models", "models"), "models")
    dbs[key] = db


def resolve_db(key=None):
    key = key or DEFAULT_KEY

    def internal_resolve():
        return session(key)

    return internal_resolve
