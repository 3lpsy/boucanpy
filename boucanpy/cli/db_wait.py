from pathlib import Path
from boucanpy.core import logger
from boucanpy.cli.base import BaseCommand


class DbWait(BaseCommand):
    name = "db-wait"
    aliases = ["dbwait"]
    description = "wait for db"
    add_log_level = True
    add_debug = True

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        from boucanpy.db.checks import is_db_up, is_db_setup

        self.db_register()
        db_up = is_db_up()
        if not db_up:
            logger.critical(
                "run@api_server.py - Database not up error. please check logs"
            )
            return self.exit(1)
        return 0
