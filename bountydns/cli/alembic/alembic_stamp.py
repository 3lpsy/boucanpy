from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.stamp import stamp
from bountydns.cli.commands.base import BaseCommand


class AlembicStamp(BaseCommand):
    name = "alembic-stamp"
    aliases = ["al-stamp"]
    description = "run alembic stamp"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        load_env("api")
        db_register(make_db_url())
        stamp(self.migration_dir)
