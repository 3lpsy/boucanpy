from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.stamp import stamp
from bountydns.cli.commands.base import BaseCommand


class AlembicStamp(BaseCommand):
    name = "alembic-stamp"
    aliases = []
    description = "run alembic stamp"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        load_env("db")
        db_register("api", make_db_url("api"))
        stamp(join(db_dir("alembic"), "api"))
