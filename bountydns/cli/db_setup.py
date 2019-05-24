from pathlib import Path
from bountydns.core import logger, load_env
from bountydns.cli.commands.base import BaseCommand

from bountydns.cli.commands.alembic import AlembicInit
from bountydns.cli.commands.alembic import AlembicUpgrade
from bountydns.cli.commands.alembic import AlembicMigrate
from bountydns.cli.commands.db_seed import DbSeed


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
            logger.info("[*] running alembic-init")
            await AlembicInit.make(self.options).run()
        logger.info("[*] running alembic upgrade")
        await AlembicUpgrade.make(self.options).run()
        logger.info("[*] running alembic migrate")
        await AlembicMigrate.make(self.options).run()
        logger.info("[*] running alembic upgrade again")
        await AlembicUpgrade.make(self.options).run()
        if self.option("seed", None):
            logger.info("[*] running db seed")
            await DbSeed.make(self.options).run()
