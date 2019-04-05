import uvicorn
from os import environ
from bountydns.core import logger, set_log_level
from bountydns.core.utils import project_dir, load_env
from bountydns.core.security import hash_password
from bountydns.cli.commands.base import BaseCommand
from bountydns.cli.commands.db_setup import DbSetup
from bountydns.db.factories import factory


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

        parser.add_argument(
            "--db-seed-env", action="store_true", help="seed data from env variables"
        )

        parser.add_argument(
            "--no-bcast-check",
            action="store_true",
            help="do not wait for broadcast service",
        )
        return parser

    async def run(self):
        args = ["bountydns.api.main:api"]
        kwargs = self.get_kwargs()
        self.load_env("api")

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
            await DbSetup.make(self.options).run()

        if not self.option("no_db_check", False):
            db_setup = is_db_setup()
            if not db_setup:
                logger.critical("database not setup error. please check logs")
                return self.exit(1)

        from bountydns.broadcast import is_broadcast_up

        if not self.option("no_bcast_check", False):
            bcast_up = await is_broadcast_up()
            if not bcast_up:
                logger.critical("broadcast (queue) not up error. please check logs")
                return self.exit(1)

        if self.option("db_seed_env", False):
            self.seed_from_env()
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

    def seed_from_env(self):
        from bountydns.core.entities.user import UserRepo

        for i in range(9):
            i = str(i)
            user_data = {}
            email_key = f"SEED_USER_{i}_EMAIL"
            email = environ.get(email_key, None)
            password_key = f"SEED_USER_{i}_PASSWORD"
            password = environ.get(password_key, None)
            superuser_key = f"SEED_USER_{i}_SUPERUSER"
            is_superuser = int(environ.get(superuser_key, 0))
            if email and password:
                hashed_password = hash_password(password)
                repo = UserRepo(db=self.session())
                if not repo.exists(email=email):
                    logger.info(f"seeding user {email}")
                    user = factory("UserFactory").create(
                        email=email,
                        hashed_password=hashed_password,
                        is_superuser=is_superuser,
                    )
                else:
                    logger.info(f"seeded user {email} already exists")
