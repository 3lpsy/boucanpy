from alembic import command
from bountydns.db.migrate.config import get_config


def history(directory=None, rev_range=None, verbose=False, indicate_current=False):
    """List changeset scripts in chronological order."""
    config = get_config(directory)
    command.history(
        config, rev_range, verbose=verbose, indicate_current=indicate_current
    )
