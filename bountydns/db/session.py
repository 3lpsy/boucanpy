from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from bountydns.db.pagination.query import PaginationQuery

# TODO: fix this nonsense


DEFAULT_KEY = "api"

dbs = {}
_sessions = {}
_session = sessionmaker(autocommit=False, autoflush=False, query_cls=PaginationQuery)
_scoped_session = scoped_session(_session)

# TODO: fix this, move back to single database target
def session():
    if DEFAULT_KEY in _sessions.keys():
        return _sessions[DEFAULT_KEY]
    session = dbs[DEFAULT_KEY]["Session"]()
    _sessions[DEFAULT_KEY] = session
    return session


def db_session():
    return dbs[DEFAULT_KEY]["db_session"]


def engine():
    return dbs[DEFAULT_KEY]["engine"]


def db_url():
    return dbs[DEFAULT_KEY]["url"]


def metadata():
    return dbs[DEFAULT_KEY]["metadata"]


def db_register(db_uri):
    global dbs
    engine = create_engine(db_uri)
    db = {}
    db["engine"] = engine
    _scoped_session.configure(bind=engine)
    db["Session"] = _session
    db["db_session"] = _scoped_session
    db["url"] = db_uri
    db["metadata"] = getattr(
        import_module(f"bountydns.db.models.base", "base"), "metadata"
    )
    db["models"] = getattr(import_module(f"bountydns.db.models", "models"), "models")
    dbs[DEFAULT_KEY] = db

    # setup factory
    from bountydns.db.factories.base import BaseFactory
