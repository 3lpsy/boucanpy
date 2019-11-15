from pathlib import Path
from boucanpy.core import logger
from boucanpy.cli.base import BaseCommand
from boucanpy.db.models import models


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
        self.db_register()
        failed = []
        if self.option("confirm"):
            for class_name, model in models.items():
                for item in self.session().query(model).all():
                    logger.warning(f"run@db_truncate.py - Deleting {item}")
                    try:
                        self.session().delete(item)
                        self.session().commit()
                    except Exception as e:
                        failed.append((item, e))
        else:
            logger.warning("run@db_truncate.py - You must confirm to drop data")

        if len(failed) > 0:
            logger.warning("run@db_truncate.py - Encountered errors")
            for f in failed:
                print("Failed:", item[0])
                print("Error", item[1])
