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
        parser.add_argument(
            "-t", "--api-token", required=True, action="store", help="api token"
        )
        parser.add_argument(
            "-i", "--dns-server-id", required=True, action="store", help="dns server id"
        )
        parser.add_argument(
            "-p", "--port", action="store", type=int, default=53, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        return parser

    def run(self):
        port = self.get_port()
        listen = self.get_listen()
        # TODO: thread issues?
        api_client = ApiClient(
            self.option("api_url"),
            self.option("api_token"),
            self.option("dns_server_id"),
        )
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

    def get_port(self):
        return self.option("port")

    def get_listen(self):
        return self.option("listen")
