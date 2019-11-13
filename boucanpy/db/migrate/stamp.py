from boucanpy.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def stamp(directory=None, revision="head", sql=False, tag=None):
    from alembic import command

    config = get_config(directory)
    command.stamp(config, revision, sql=sql, tag=tag)
