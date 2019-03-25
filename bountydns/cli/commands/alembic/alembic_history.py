from os.path import join
from bountydns.core.utils import db_dir, load_env
from bountydns.db.session import session, db_register
from bountydns.db.utils import make_db_url
from bountydns.db.migrate.history import history
from bountydns.cli.commands.base import BaseCommand


class AlembicHistory(BaseCommand):
    name = "alembic-history"
    aliases = []
    description = "run alembic history"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        load_env("db")
        db_register("api", make_db_url("api"))
        history(join(db_dir("alembic"), "api"))
