from bountydns.core import logger, load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.factories import factory
from bountydns.db import db_register, make_db_url


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
        load_env("db")
        db_register(make_db_url())
        logger.info("creating superuser")
        super = factory("SuperUserFactory").create(email="jim@jim.jim")
        logger.info("creating zones")

        zone = factory("ZoneFactory").create(domain="example.com", ip="127.0.1.1")
        zone2 = factory("ZoneFactory").create(domain="potato.com", ip="127.0.1.1")

        logger.info("creating api_tokens")

        api_token = factory("ApiTokenFactory").create()
        api_token2 = factory("ApiTokenFactory").create()

        logger.info("creating dns_requests")
        dns_request = factory("DnsRequestFactory").create(zone_id=zone.id)
        dns_request = factory("DnsRequestFactory").create(zone_id=zone2.id)
        dns_request = factory("DnsRequestFactory").create()
        dns_request = factory("DnsRequestFactory").create()
