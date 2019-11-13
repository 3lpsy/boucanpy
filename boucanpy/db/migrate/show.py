from boucanpy.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def show(directory=None, revision="head"):
    from alembic import command

    """Show the revision denoted by the given symbol."""
    config = get_config(directory)
    command.show(config, revision)
