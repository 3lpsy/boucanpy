import os
from pathlib import Path
from time import sleep
from dnslib.server import DNSServer
from bountydns.core import logger
from bountydns.dns.resolver import Resolver
from bountydns.dns.logger import DNSLogger
from bountydns.dns.handler import DNSHandler

from bountydns.cli.commands.base import BaseCommand
from bountydns.dns.api_client import ApiClient


class DnsServer(BaseCommand):
    name = "dns-server"
    aliases = ["dns"]
    description = "run dns server"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-a",
            "--api-url",
            default="http://127.0.0.1:8080",
            action="store",
            help="api url",
        )
        parser.add_argument("-t", "--api-token", action="store", help="api token")
        parser.add_argument(
            "-p", "--port", action="store", type=int, default=53, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        parser.add_argument(
            "--sync-api-token",
            action="store_true",
            help="sync api token back to database",
        )
        return parser

    async def run(self):
        port = self.get_port()
        listen = self.get_listen()
        # TODO: thread issues?
        api_client = ApiClient(self.get_api_url(), self.get_api_token())

        if not api_client.wait_for_up():
            logger.critical("could not connect to api. quitting")
            self.exit(1)

        if self.option("sync_api_token"):
            api_client.sync_api_token()

        resolver = Resolver(api_client)
        udp_server = DNSServer(
            resolver,
            address=listen,
            port=port,
            handler=DNSHandler,
            logger=DNSLogger(api_client),
        )
        tcp_server = DNSServer(
            resolver,
            address=listen,
            port=port,
            tcp=True,
            handler=DNSHandler,
            logger=DNSLogger(api_client),
        )

        logger.info("starting DNS server on port %d", port)
        udp_server.start_thread()
        tcp_server.start_thread()

        try:
            while udp_server.isAlive():
                sleep(1)
        except KeyboardInterrupt:
            pass

    def get_api_url(self):
        if os.environ.get("API_URL", None):
            return os.environ.get("API_URL")
        return self.option("api_url")

    def get_api_token(self):
        if os.environ.get("API_TOKEN", None):
            return os.environ.get("API_TOKEN")
        if self.option("api_token", None):
            return self.option("api_token")
        logger.critical("api token required")
        self.exit(1)

    def get_port(self):
        return self.option("port")

    def get_listen(self):
        return self.option("listen")
