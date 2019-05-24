from pathlib import Path
from bountydns.core import logger
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models import models


class DbTruncate(BaseCommand):
    name = "db-truncate"
    aliases = ["truncate"]
    description = "truncate db"
    add_log_level = True
    add_debug = True

    @classmethod
    def parser(cls, parser):
        parser.add_argument("-c", "--confirm", action="store_true", help="seed data")
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        failed = []
        if self.option("confirm"):
            for model in models:
                for item in self.session().query(model).all():
                    logger.info(f"deleting {item}")
                    try:
                        self.session().delete(item)
                        self.session().commit()
                    except Exception as e:
                        failed.append((item, e))
        else:
            logger.warning("You must confirm to drop data")

        if len(failed) > 0:
            logger.critical("encountered errors")
            for f in failed:
                print("Failed:", item[0])
                print("Error", item[1])
