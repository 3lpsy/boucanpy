import uvicorn
from bountydns.core import logger, set_log_level
from bountydns.core.utils import project_dir, load_env
from .base import BaseCommand


class ApiServer(BaseCommand):
    name = "apiserver"
    aliases = ["api"]
    description = "run api server"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-p", "--port", action="store", type=int, default=8080, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        parser.add_argument("-d", "--debug", action="store_true", help="debug")
        parser.add_argument("-r", "--reload", action="store_true", help="reload")
        parser.add_argument("-w", "--workers", action="store", help="workers")
        parser.add_argument(
            "-i",
            "--import-check",
            action="store_true",
            help="perform an import check of the api instance",
        )

        return parser

    def run(self):
        args = ["bountydns.api.server.main:api"]
        kwargs = self.get_kwargs()
        load_env("db")
        load_env("api")

        if self.option("import_check", False):
            logger.info("performing import check")
            from bountydns.api.server.main import api
        logger.critical("starting api server with options: {}".format(str(kwargs)))
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

    def get_log_level(self):
        if self.option("debug", None):
            level = "debug"
        elif self.option("log_level", None):
            level = self.option("log_level")
        set_log_level(level)
        return level

    def get_reload(self):
        if self.option("debug", None):
            return True
        return bool(self.option("reload"))

    def get_workers(self):
        if self.option("debug", None) or self.option("reload", None):
            logger.critical("Canot use debug or reload with workers. Skipping.")
            return None
        return self.option("workers", 5)
