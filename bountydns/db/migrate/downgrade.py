from bountydns.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def downgrade(directory=None, revision="-1", sql=False, tag=None, x_arg=None):
    from alembic import command

    """Revert to a previous version"""
    config = get_config(directory, x_arg=x_arg)
    if sql and revision == "-1":
        revision = "head:-1"
    command.downgrade(config, revision, sql=sql, tag=tag)
