from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.upgrade import upgrade
from bountydns.cli.commands.base import BaseCommand


class AlembicUpgrade(BaseCommand):
    name = "alembic-upgrade"
    aliases = ["al-upgrade"]
    description = "run alembic upgrade"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        load_env("db")
        db_register(make_db_url())
        upgrade(join(db_dir("alembic"), "api"))
