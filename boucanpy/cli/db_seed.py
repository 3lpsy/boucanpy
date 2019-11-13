from boucanpy.core import logger
from boucanpy.cli.base import BaseCommand
from boucanpy.db.factories import factory
import uuid


class DbSeed(BaseCommand):
    name = "db-seed"
    aliases = ["seed"]
    description = "seed db"
    add_log_level = True
    add_debug = True

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-t", "--target", action="store", default="dev", help="target"
        )
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        self.db_register()

        if self.option("target", False) == False:
            self.set_option("target", "dev")

        if self.option("target") == "env":
            # self.load_env("seed")
            logger.info(f"run@db_seed.py - Seeding {self.option('target')}")
            raise NotImplementedError()  # seed based on env vars

        elif self.option("target") == "dev":
            logger.info(f"run@db_seed.py - Seeding {self.option('target')}")
            logger.info("run@db_seed.py - reating superuser")
            super = factory("SuperUserFactory").create(email="jim@jim.com")

            logger.info("run@db_seed.py - Creating normal user")
            norm = factory("UserFactory").create(email="norm@jim.com")

            logger.info("run@db_seed.py - Creating dns_server")

            _dns_server = factory("DnsServerFactory").create(name="mydnsserver")

            dns_server = factory("DnsServerFactory").create()

            logger.info("run@db_seed.py - Creating http_server")

            _http_server = factory("HttpServerFactory").create(name="myhttpserver")

            http_server = factory("HttpServerFactory").create()

            logger.info("run@db_seed.py - Creating zones")

            zone = factory("ZoneFactory").create(domain="othersite.com", ip="127.0.1.1")

            zone2 = factory("ZoneFactory").create(
                domain="friends4life.com",
                ip="127.0.1.1",
                dns_server=dns_server,
                http_server=http_server,
            )

            zone3 = factory("ZoneFactory").create(
                domain="differentzone.com", ip="127.0.1.1"
            )

            logger.info("run@db_seed.py - Creating api_tokens")

            factory("ApiTokenFactory").create(dns_server=dns_server)
            factory("ApiTokenFactory").create(http_server=http_server)
            factory("ApiTokenFactory").create(
                dns_server=dns_server, http_server=http_server
            )

            logger.info("run@db_seed.py - Creating dns_requests")

            for i in range(35):
                factory("DnsRequestFactory").create(dns_server=dns_server, zone=zone2)

            for i in range(35):
                factory("DnsRequestFactory").create(dns_server=dns_server, zone=zone3)

            logger.info("run@db_seed.py - Creating dns_records")

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone)

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone2)

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone3)

            logger.info("run@db_seed.py - Creating http_requests")

            for i in range(35):
                factory("HttpRequestFactory").create(
                    http_server=http_server, zone=zone2
                )

            for i in range(35):
                factory("HttpRequestFactory").create(
                    http_server=http_server, zone=zone3
                )
        else:
            logger.critical("run@db_seed.py - invalid target set for seeder")
            self.exit(1)
