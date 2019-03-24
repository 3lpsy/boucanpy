import os
from pathlib import Path
from time import sleep
from dnslib.server import DNSServer
from bountydns.core import logger
from bountydns.dns.resolver import Resolver
from bountydns.dns.logger import DnsLogger

from .base import BaseCommand


class DnsServer(BaseCommand):
    name = "dnsserver"
    aliases = ["dns"]
    description = "run dns server"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-z", "--zone", action="append", help="zones to answer (only domain:ip)"
        )
        parser.add_argument(
            "-Z",
            "--zone-file",
            action="store",
            help="file (txt) with zones to answer (only domain:ip)",
        )
        parser.add_argument(
            "-u", "--upstream", action="store", help="upstream dns server"
        )
        parser.add_argument("-a", "--api-url", action="store", help="callback api url")
        parser.add_argument(
            "-t", "--api-token", action="store", help="callback api token"
        )
        parser.add_argument(
            "-p", "--port", action="store", type=int, default=53, help="listen port"
        )
        parser.add_argument(
            "-l", "--listen", action="store", default="127.0.0.1", help="bind address"
        )
        return parser

    def run(self):
        zones = self.get_zones()
        upstream = self.get_upstream()
        api_url = self.get_api_url()
        api_token = self.get_api_token()
        port = self.get_port()
        listen = self.get_listen()

        resolver = Resolver(zones, upstream, api_url, api_token)
        udp_server = DNSServer(resolver, address=listen, port=port, logger=DnsLogger())
        tcp_server = DNSServer(
            resolver, address=listen, port=port, tcp=True, logger=DnsLogger()
        )

        logger.info(
            'starting DNS server on port %d, upstream DNS server "%s", %d zones',
            port,
            upstream,
            len(zones),
        )
        udp_server.start_thread()
        tcp_server.start_thread()

        try:
            while udp_server.isAlive():
                sleep(1)
        except KeyboardInterrupt:
            pass

    def get_zones(self):
        zones = []
        if self.option("zone", None):
            for z in self.option("zone"):
                zp = z.split(":")
                zones.append((zp[0], zp[1]))
        if self.option("zone_file"):
            logger.info('loading zones from zone file "%s"', self.option("zone_file"))
            zones = zones + self.read_zone_file(self.option("zone_file"))
        if os.getenv("ZONE_FILE", None):
            logger.info('loading zones from zone file "%s"', os.getenv("ZONE_FILE"))
            zones = zones + self.read_zone_file(os.getenv("ZONE_FILE"))
        if os.getenv("ZONES", None):
            zones = zones + [
                (zp.split(":")[0], zp.split(":")[1])
                for zp in os.getenv("ZONES").split(",")
            ]
        return zones

    def read_zone_file(self, zone_file):
        zones = []
        with open(str(Path(zone_file).resolve()), "r") as f:
            for l in f.readlines():
                if not l.startswith("#"):
                    zp = l.rstrip("\r\t\n").split(":")
                    zones.append((zp[0], zp[1]))
        return zones

    def get_upstream(self):
        # TODO: Customize this
        return "208.67.222.222"

    def get_api_url(self):
        # TODO: Finish this
        return ""

    def get_api_token(self):
        # TODO: Finish this
        return ""

    def get_port(self):
        return self.option("port")

    def get_listen(self):
        return self.option("listen")
