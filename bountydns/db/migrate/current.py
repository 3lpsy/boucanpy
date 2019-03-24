from alembic import command
from bountydns.db.migrate.config import get_config


def current(directory=None, verbose=False, head_only=False):
    """Display the current revision for each database."""
    config = get_config(directory)
    command.current(config, verbose=verbose, head_only=head_only)
