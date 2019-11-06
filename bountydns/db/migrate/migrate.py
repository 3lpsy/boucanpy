import os
from bountydns.db.migrate.config import get_config

# late import of alembic because it destroys loggers
def migrate(
    directory=None,
    message=None,
    sql=False,
    head="head",
    splice=False,
    branch_label=None,
    version_path=None,
    rev_id=None,
    x_arg=None,
):
    from alembic import command

    """Alias for 'revision --autogenerate'"""

    config = get_config(directory, opts=["autogenerate"], x_arg=x_arg)
    command.revision(
        config,
        message,
        autogenerate=True,
        sql=sql,
        head=head,
        splice=splice,
        branch_label=branch_label,
        version_path=version_path,
        rev_id=rev_id,
    )
