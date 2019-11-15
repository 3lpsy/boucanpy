from os.path import join
from boucanpy.core.utils import db_dir
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.upgrade import upgrade
from boucanpy.cli.base import BaseCommand


class AlembicUpgrade(BaseCommand):
    name = "alembic-upgrade"
    aliases = ["al-upgrade"]
    description = "run alembic upgrade"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        db_register(make_db_url())
        upgrade(self.migration_dir)
