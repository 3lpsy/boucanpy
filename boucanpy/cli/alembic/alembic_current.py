from os.path import join
from boucanpy.core.utils import db_dir
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.current import current
from boucanpy.cli.base import BaseCommand


class AlembicCurrent(BaseCommand):
    name = "alembic-current"
    aliases = ["al-current"]
    description = "run alembic current"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        db_register(make_db_url())
        current(self.migration_dir)
