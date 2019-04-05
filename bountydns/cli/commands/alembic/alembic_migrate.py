from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.migrate import migrate
from bountydns.cli.commands.base import BaseCommand


class AlembicMigrate(BaseCommand):
    name = "alembic-migrate"
    aliases = ["al-migrate"]
    description = "run alembic migrate"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        load_env("api")
        db_register(make_db_url())
        migrate(self.migration_dir)
