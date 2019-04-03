import uvicorn
from bountydns.core import logger, set_log_level
from bountydns.core.utils import project_dir, load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.cli.commands.db_setup import DbSetup


class ApiServer(BaseCommand):
    name = "api-server"
    aliases = ["api"]
    description = "run api server"
    add_log_level = True
    add_debug = True

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-p", "--port", action="store", type=int, default=8080, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        parser.add_argument("-r", "--reload", action="store_true", help="reload")
        parser.add_argument("-w", "--workers", action="store", help="workers")
        parser.add_argument(
            "-i",
            "--import-check",
            action="store_true",
            help="perform an import check of the api instance",
        )

        parser.add_argument(
            "--no-db-check", action="store_true", help="do not wait for database"
        )

        parser.add_argument(
            "--db-setup", action="store_true", help="run db setup before start"
        )
        return parser

    def run(self):
        args = ["bountydns.api.main:api"]
        kwargs = self.get_kwargs()
        self.load_env("db", "api", "broadcast")

        if self.option("import_check", False):
            logger.info("performing import check")
            from bountydns.api.main import api
        logger.critical("starting api server with options: {}".format(str(kwargs)))
        from bountydns.db.checks import is_db_up, is_db_setup

        if not self.option("no_db_check", False):
            self.db_register()
            db_up = is_db_up()
            if not db_up:
                logger.critical("database not up error. please check logs")
                return self.exit(1)

        if self.option("db_setup"):
            logger.critical("running database migration")
            DbSetup.make(self.options).run()

        if not self.option("no_db_check", False):
            db_setup = is_db_setup()
            if not db_setup:
                logger.critical("database not setup error. please check logs")
                return self.exit(1)

        return uvicorn.run(*args, **kwargs)

    def get_kwargs(self):
        kwargs = {
            "host": self.option("listen"),
            "port": self.option("port"),
            "log_level": self.get_log_level(),
        }
        if self.get_reload():
            kwargs["reload"] = self.get_reload()
            kwargs["reload_dirs"] = [project_dir()]

        elif self.get_workers():
            kwargs["workers"] = self.get_workers()

        return kwargs

    def get_reload(self):
        if self.option("debug", None):
            return True
        return bool(self.option("reload"))

    def get_workers(self):
        if self.option("debug", None) or self.option("reload", None):
            logger.critical("Canot use debug or reload with workers. Skipping.")
            return None
        return self.option("workers", 5)
