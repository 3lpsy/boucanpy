from os import environ
from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from bountydns.db.pagination.query import PaginationQuery
from .events import db_register_model_events, db_register_search_events

# TODO: fix this nonsense

DEFAULT_KEY = "api"

dbs = {}
_sessions = {}
_session = sessionmaker(autocommit=False, autoflush=False, query_cls=PaginationQuery)
_scoped_session = scoped_session(_session)

import traceback
import inspect

# TODO: fix this, move back to single database target
def session():
    if DEFAULT_KEY in _sessions.keys():
        return _sessions[DEFAULT_KEY]
    session = dbs[DEFAULT_KEY]["Session"]()
    _sessions[DEFAULT_KEY] = session
    return session


# Depends(session) resolves on different threadpool. Use Depends(async_session) for same threadpool
async def async_session():
    return session()


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
    models = getattr(import_module(f"bountydns.db.models", "models"), "models")
    db["models"] = models.values()
    dbs[DEFAULT_KEY] = db
    # setup events

    if int(environ.get("BROADCAST_ENABLED", 0)) == 1:
        db_register_model_events(models)

    from bountydns.db.search.mixin import SearchableMixin

    db_register_search_events(_scoped_session, SearchableMixin)

    # setup factory / avoid circular imports /
    from bountydns.db.factories.base import BaseFactory
