from alembic import command
from bountydns.db.migrate.config import get_config


def show(directory=None, revision="head"):
    """Show the revision denoted by the given symbol."""
    config = get_config(directory)
    command.show(config, revision)
