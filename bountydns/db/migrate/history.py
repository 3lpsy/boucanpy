from bountydns.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def history(directory=None, rev_range=None, verbose=False, indicate_current=False):
    from alembic import command

    """List changeset scripts in chronological order."""
    config = get_config(directory)
    command.history(
        config, rev_range, verbose=verbose, indicate_current=indicate_current
    )
