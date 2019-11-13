from os.path import join
from boucanpy.core.utils import db_dir, load_env
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.show import show
from boucanpy.cli.base import BaseCommand


class AlembicShow(BaseCommand):
    name = "alembic-show"
    aliases = ["al-show"]
    description = "run alembic show"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        db_register(make_db_url())
        show(self.migration_dir)
