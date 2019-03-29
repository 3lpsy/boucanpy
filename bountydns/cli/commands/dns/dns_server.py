import os
from pathlib import Path
from time import sleep
from dnslib.server import DNSServer
from bountydns.core import logger
from bountydns.dns.resolver import Resolver
from bountydns.dns.logger import DnsLogger

from bountydns.cli.commands.base import BaseCommand


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
            "-p", "--port", action="store", type=int, default=53, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        return parser

    def run(self):
        api_url = self.option("api_url")
        api_token = self.option("api_token")
        port = self.get_port()
        listen = self.get_listen()

        resolver = Resolver(api_url, api_token)
        udp_server = DNSServer(
            resolver, address=listen, port=port, logger=DnsLogger(api_url, api_token)
        )
        tcp_server = DNSServer(
            resolver,
            address=listen,
            port=port,
            tcp=True,
            logger=DnsLogger(api_url, api_token),
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
