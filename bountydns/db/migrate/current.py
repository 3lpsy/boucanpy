from bountydns.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def current(directory=None, verbose=False, head_only=False):
    from alembic import command

    """Display the current revision for each database."""
    config = get_config(directory)
    command.current(config, verbose=verbose, head_only=head_only)
