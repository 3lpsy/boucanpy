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
        return parser

    def run(self):
        self.load_env("api", "db")
        self.db_register()

        logger.info("creating superuser")
        super = factory("SuperUserFactory").create(email="jim@jim.jim")
        logger.info("creating zones")

        zone = factory("ZoneFactory").create(domain="example.com", ip="127.0.1.1")
        dns_server_name = uuid.uuid4()
        zone2 = factory("ZoneFactory").create(
            domain="potato.com", ip="127.0.1.1", dns_server_name=dns_server_name
        )

        logger.info("creating api_tokens")

        api_token = factory("ApiTokenFactory").create()
        api_token2 = factory("ApiTokenFactory").create()

        logger.info("creating dns_requests")
        dns_request = factory("DnsRequestFactory").create(zone_id=zone.id)
        dns_request = factory("DnsRequestFactory").create(zone_id=zone2.id)
        dns_request = factory("DnsRequestFactory").create(
            dns_server_name=dns_server_name
        )
        dns_request = factory("DnsRequestFactory").create(
            dns_server_name=dns_server_name
        )
