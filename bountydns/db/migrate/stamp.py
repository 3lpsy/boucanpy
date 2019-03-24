from alembic import command
from bountydns.db.migrate.config import get_config


def stamp(directory=None, revision="head", sql=False, tag=None):
    config = get_config(directory)
    command.stamp(config, revision, sql=sql, tag=tag)
