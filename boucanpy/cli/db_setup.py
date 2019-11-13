from pathlib import Path
from boucanpy.core import logger, load_env
from boucanpy.cli.base import BaseCommand

from boucanpy.cli.alembic import AlembicInit
from boucanpy.cli.alembic import AlembicUpgrade
from boucanpy.cli.alembic import AlembicMigrate
from boucanpy.cli.db_seed import DbSeed


class DbSetup(BaseCommand):
    name = "db-setup"
    aliases = ["setup"]
    description = "setup db"
    add_log_level = True
    add_debug = True

    @classmethod
    def parser(cls, parser):
        parser.add_argument("-s", "--seed", action="store_true", help="seed data")
        return parser

    async def run(self):
        if not Path(AlembicInit.migration_dir).is_dir():
            logger.info("run@db_setup.py - Running alembic-init")
            await AlembicInit.make(self.options).run()
        logger.info("run@db_setup.py - Running alembic upgrade")
        await AlembicUpgrade.make(self.options).run()
        logger.info("run@db_setup.py - Running alembic migrate")
        await AlembicMigrate.make(self.options).run()
        logger.info("run@db_setup.py - Running alembic upgrade again")
        await AlembicUpgrade.make(self.options).run()
        if self.option("seed", None):
            logger.info("run@db_setup.py - Running db seed")
            await DbSeed.make(self.options).run()
