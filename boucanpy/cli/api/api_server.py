import uvicorn

from uvicorn import Config as UvicornConfig, Server as UvicornServer
from uvicorn.supervisors import Multiprocess, StatReload


from os import environ
from boucanpy.core import logger, set_log_level
from boucanpy.core.utils import project_dir
from boucanpy.core.security import hash_password
from boucanpy.cli.base import BaseCommand
from boucanpy.cli.db_setup import DbSetup
from boucanpy.cli.db_wait import DbWait
from boucanpy.db.factories import factory


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
        parser.add_argument(
            "--force-exit",
            action="store_true",
            help="force exit on reload, useful for restarting websockets in development",
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
            "--db-seed", action="store_true", help="seed additional fake data"
        )

        parser.add_argument(
            "--no-bcast-check",
            action="store_true",
            help="do not wait for broadcast service",
        )
        return parser

    async def run(self):
        app = "boucanpy.api.main:api"
        kwargs = self.get_kwargs()
        env = self.option("env")
        self.load_env(f"api.{env}")

        if self.should_import_check():
            logger.info("run@api_server.py - Performing import check")
            from boucanpy.api.main import api

        logger.critical(
            "run@api_server.py - Starting api server with options: {}".format(
                str(kwargs)
            )
        )
        from boucanpy.db.checks import is_db_up, is_db_setup

        # alembic just destroys the loggers, it's annoying
        if self.should_db_check():
            logger.info("run@api_server.py - Waiting for database service to be up")
            db_wait_options = self._args_to_dict(self.options)
            await DbWait(db_wait_options).run()

        if self.option("db_setup"):
            logger.critical("run@api_server.py - Running database migration")
            db_setup_options = self._args_to_dict(self.options)
            if self.option("db_seed"):
                db_setup_options["seed"] = True
            await DbSetup(db_setup_options).run()

        if self.should_db_check():
            logger.info(
                "run@api_server.py - Checking if application database is setup and configured"
            )

            db_setup = is_db_setup()
            if not db_setup:
                logger.critical(
                    "run@api_server.py - Database not setup error. please check logs"
                )
                return self.exit(1)

        from boucanpy.broadcast import is_broadcast_up

        if self.should_bcast_check():
            bcast_up = await is_broadcast_up()
            if not bcast_up:
                logger.critical(
                    "run@api_server.py - Broadcast (queue) not up error. please check logs"
                )
                return self.exit(1)

        if self.option("db_seed_env", False):
            self.seed_from_env()

        # taken from uvicorn/main.py:run

        logger.debug("run@api_server.py - Building Uvicorn Config and Server")
        config = UvicornConfig(app, log_config=self.get_uvicorn_logging(), **kwargs)
        server = UvicornServer(config=config)
        if self.option("force_exit"):
            server.force_exit = True

        if isinstance(app, str) and (config.debug or config.reload):
            logger.warning(f"run@api_server.py - Running boucanpy api in dev mode...")
            sock = config.bind_socket()
            supervisor = StatReload(config)
            return supervisor.run(server.run, sockets=[sock])
        elif config.workers > 1:
            sock = config.bind_socket()
            supervisor = Multiprocess(config)
            logger.warning(
                f"run@api_server.py - Running boucanpy api in worker mode..."
            )
            return supervisor.run(server.run, sockets=[sock])
        else:
            sockets = None
            logger.warning(
                f"run@api_server.py - Running boucanpy api in standard mode..."
            )
            return await server.serve(sockets=sockets)

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
            kwargs["workers"] = int(self.get_workers())

        if self.option("debug", None):
            kwargs["debug"] = True
        return kwargs

    def get_reload(self):
        if self.option("debug", None):
            return True
        return bool(self.option("reload"))

    def get_workers(self):
        if self.option("debug", None) or self.option("reload", None):
            logger.critical(
                "get_workers@api_server.py - Cannot use debug or reload with workers. Skipping."
            )
            return None
        return self.option("workers", 5)

    def should_import_check(self):
        return (
            self.option("import_check", False)
            or self.env("API_IMPORT_CHECK", 0, int_=True) == 1
        )

    def should_db_check(self):
        if not self.option("no_db_check", False):
            return True
        elif self.env("API_NO_DB_CHECK", 1, int_=True) == 0:
            return True
        return False

    def should_bcast_check(self):
        if self.env("BROADCAST_ENABLED", 0, int_=True) == 0:
            return False
        elif self.option("no_bcast_check", False):
            return False
        elif self.env("API_NO_BROADCAST_CHECK", 1, int_=True) == 0:
            return False
        return True

    def seed_from_env(self):
        from boucanpy.core.user import UserRepo
        from boucanpy.core.zone import ZoneRepo
        from boucanpy.core.dns_server import DnsServerRepo
        from boucanpy.db.session import _scoped_session

        session = _scoped_session

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
                email = email.lower()
                hashed_password = hash_password(password)
                repo = UserRepo(db=session)
                if not repo.exists(email=email):
                    logger.info(f"seed_from_env@api_server.py - seeding user {email}")
                    user = factory("UserFactory", session=session).create(
                        email=email,
                        hashed_password=hashed_password,
                        is_superuser=is_superuser,
                    )
                else:
                    logger.info(
                        f"seed_from_env@api_server.py - Seeded user {email} already exists"
                    )

        for i in range(9):
            i = str(i)
            name_key = f"SEED_DNS_SERVER_{i}_NAME"
            name = environ.get(name_key, None)
            if name:
                repo = DnsServerRepo(db=session)
                if not repo.exists(name=name):
                    logger.info(f"seed_from_env@api_server.py - Seeding domain {name}")
                    domain = factory("DnsServerFactory", session=session).create(
                        name=name
                    )

        for i in range(9):
            i = str(i)
            ip_key = f"SEED_ZONE_{i}_IP"
            domain_key = f"SEED_ZONE_{i}_DOMAIN"
            dns_server_name_key = f"SEED_ZONE_{i}_DNS_SERVER_NAME"
            ip = environ.get(ip_key, None)
            domain = environ.get(domain_key, None)
            if domain:
                domain = domain.lower()
            dns_server_name = environ.get(dns_server_name_key, None)
            if ip and domain:
                if dns_server_name:
                    dns_server_repo = DnsServerRepo(db=session)
                    if dns_server_repo.exists(name=dns_server_name):
                        dns_server = dns_server_repo.results()
                    else:
                        logger.info(
                            f"seed_from_env@api_server.py - Seeding dns server as zone dependency: {name}"
                        )
                        dns_server = factory(
                            "DnsServerFactory", session=session
                        ).create(name=dns_server_name)
                    factory("ZoneFactory", session=session).create(
                        ip=ip, domain=domain, dns_server=dns_server
                    )
                else:
                    repo = ZoneRepo(db=session)
                    if not repo.exists(ip=ip, domain=domain):
                        logger.info(
                            f"seed_from_env@api_server.py - Seeding zone without dns server: {ip}, {domain}"
                        )
                        factory("GlobalZoneFactory", session=session).create(
                            ip=ip, domain=domain
                        )

