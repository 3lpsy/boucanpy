from os.path import join
from boucanpy.core.utils import db_dir, load_env
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.history import history
from boucanpy.cli.base import BaseCommand


class AlembicHistory(BaseCommand):
    name = "alembic-history"
    aliases = ["al-history"]
    description = "run alembic history"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        db_register(make_db_url())
        history(self.migration_dir)
