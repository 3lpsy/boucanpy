from bountydns.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def upgrade(directory=None, revision="head", sql=False, tag=None, x_arg=None):
    from alembic import command

    """Upgrade to a later version"""
    config = get_config(directory, x_arg=x_arg)
    command.upgrade(config, revision, sql=sql, tag=tag)
