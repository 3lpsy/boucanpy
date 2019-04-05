from bountydns.core import logger
from bountydns.cli.commands.base import BaseCommand
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
        self.load_env("api")
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
            super = factory("SuperUserFactory").create(email="jim@jim.jim")
            logger.info("creating zones")
            zone = factory("ZoneFactory").create(domain="example.com", ip="127.0.1.1")
            dns_server_name = uuid.uuid4()
            zone2 = factory("ZoneFactory").create(
                domain="potato.com", ip="127.0.1.1", dns_server_name=dns_server_name
            )
            dns_server_name2 = uuid.uuid4()
            zone3 = factory("ZoneFactory").create(
                domain="differentzone.com",
                ip="127.0.1.1",
                dns_server_name=dns_server_name2,
            )

            logger.info("creating api_tokens")

            for i in range(65):
                factory("ApiTokenFactory").create(dns_server_name=dns_server_name)

            logger.info("creating dns_requests")
            dns_request = factory("DnsRequestFactory").create(zone_id=zone.id)
            dns_request = factory("DnsRequestFactory").create(zone_id=zone2.id)

            for i in range(35):
                dns_request = factory("DnsRequestFactory").create(
                    dns_server_name=dns_server_name
                )

            for i in range(35):
                dns_request = factory("DnsRequestFactory").create(
                    dns_server_name=dns_server_name2
                )
        else:
            print("invalid target set for seeder")
            self.exit(1)
