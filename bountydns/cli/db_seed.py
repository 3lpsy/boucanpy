from bountydns.core import logger
from bountydns.cli.base import BaseCommand
from bountydns.db.factories import factory
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
            logger.info(f"seeding {self.option('target')}")
            raise NotImplementedError()  # seed based on env vars

        elif self.option("target") == "dev":
            logger.info(f"seeding {self.option('target')}")

            logger.info("creating superuser")
            super = factory("SuperUserFactory").create(email="jim@jim.com")
            logger.info("creating normal user")
            norm = factory("UserFactory").create(email="norm@jim.com")

            logger.info("creating zones")
            zone = factory("ZoneFactory").create(domain="othersite.com", ip="127.0.1.1")
            dns_server = factory("DnsServerFactory").create()

            zone2 = factory("ZoneFactory").create(
                domain="friends4life.com", ip="127.0.1.1", dns_server=dns_server
            )

            zone3 = factory("ZoneFactory").create(
                domain="differentzone.com", ip="127.0.1.1"
            )

            logger.info("creating api_tokens")

            for i in range(65):
                factory("ApiTokenFactory").create(dns_server=dns_server)

            logger.info("creating dns_requests")

            for i in range(35):
                factory("DnsRequestFactory").create(dns_server=dns_server, zone=zone2)

            for i in range(35):
                factory("DnsRequestFactory").create(dns_server=dns_server, zone=zone3)

            logger.info("creating dns_records")

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone)

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone2)

            for i in range(3):
                factory("DnsRecordFactory").create(zone=zone3)
        else:
            print("invalid target set for seeder")
            self.exit(1)
