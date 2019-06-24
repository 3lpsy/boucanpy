# http://alexmic.net/flask-sqlalchemy-pytest/
from os import unlink
import pytest
from os.path import join, exists

from sqlalchemy.orm import scoped_session

from bountydns.core import load_env
from bountydns.core.utils import db_dir, project_dir, storage_dir

load_env("api.test")

from bountydns.api.api import api
from bountydns.db.session import session as _api_session
from bountydns.db.session import _session  # sessionmaker
from bountydns.db import metadata as _metadata
from bountydns.db import engine as _engine

from bountydns.db.utils import get_resolved_db_path
from starlette.testclient import TestClient

from bountydns.db.migrate.upgrade import upgrade
import logging


@pytest.fixture
def setlog(caplog):
    caplog.set_level(logging.INFO)


@pytest.fixture(scope="session")
def client(request):

    _client = TestClient(api)
    return _client


@pytest.fixture(scope="session")
def engine(client, request):
    """Session-wide test database."""
    DB_PATH = get_resolved_db_path()

    if exists(DB_PATH):
        unlink(DB_PATH)

    migration_dir = join(db_dir("alembic"), "api")
    e = _engine()

    def teardown():
        _metadata().drop_all(bind=e)
        unlink(DB_PATH)

    upgrade(migration_dir)

    request.addfinalizer(teardown)

    return e


@pytest.fixture(scope="function")
def session(engine, request):
    """Creates a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    s = _session(**options)  # calls session maker
    scoped = scoped_session(s)

    def teardown():
        transaction.rollback()
        connection.close()
        scoped.remove()

    request.addfinalizer(teardown)
    return scoped
