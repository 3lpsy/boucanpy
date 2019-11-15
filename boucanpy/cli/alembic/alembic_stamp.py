from os.path import join
from boucanpy.core.utils import db_dir
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.stamp import stamp
from boucanpy.cli.base import BaseCommand


class AlembicStamp(BaseCommand):
    name = "alembic-stamp"
    aliases = ["al-stamp"]
    description = "run alembic stamp"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        db_register(make_db_url())
        stamp(self.migration_dir)
