from os.path import join
from boucanpy.core.utils import db_dir
from boucanpy.db.session import session, db_register
from boucanpy.db.utils import make_db_url
from boucanpy.db.migrate.downgrade import downgrade
from boucanpy.cli.base import BaseCommand


class AlembicDowngrade(BaseCommand):
    name = "alembic-downgrade"
    aliases = ["al-downgrade"]
    description = "run alembic downgrade"
    migration_dir = join(db_dir("alembic"), "api")

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        db_register(make_db_url())
        downgrade(self.migration_dir)
