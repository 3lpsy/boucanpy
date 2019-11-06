import os
from pathlib import Path
from time import sleep
from dnslib.server import DNSServer
from bountydns.core import logger
from bountydns.dns.resolver import Resolver
from bountydns.dns.logger import DNSLogger
from bountydns.dns.handler import DNSHandler

from bountydns.cli.base import BaseCommand
from bountydns.dns.api_client import ApiClient


class DnsServer(BaseCommand):
    name = "dns-server"
    aliases = ["dns"]
    description = "run dns server"
    add_log_level = True
    add_debug = True

    def __init__(self, *args, **kwargs):
        self.api_client = None
        self.resolver = None
        self.udp_server = None
        self.tcp_server = None
        super().__init__(*args, **kwargs)

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
            "--no-sync", action="store_true", help="sync api token back to database"
        )

        parser.add_argument(
            "--no-ssl-verify",
            action="store_true",
            help="skip ssl verify in the dns server's api client",
        )

        parser.add_argument(
            "-r",
            "--refresh-ttl",
            type=int,
            default=3600,
            action="store",
            help="time to wait before polling for new records",
        )
        return parser

    async def run(self):

        # TODO: thread issues?
        verify_ssl = True
        if bool(self.option("no_verify_ssl")):
            verify_ssl = False

        self.api_client = ApiClient(
            self.get_api_url(), self.get_api_token(), verify_ssl=verify_ssl
        )

        if not self.api_client.wait_for_up():
            logger.critical("run@dns_server.py - Could not connect to api. quitting")
            self.exit(1)

        if self.option("no_sync"):
            logger.info("run@dns_server.py - Skipping syncing api token")
        else:
            self.api_client.sync()

        self.boot()

        self.start_servers()

        try:
            count = 0
            while self.udp_server.isAlive():
                if count > 0 and count % self.option("refresh_ttl") == 0:
                    if self.api_client.refresh_zones_if_needed():
                        logger.critical(
                            "run@dns_server.py - API Client found new or changed zones. Stopping servers..."
                        )
                        # TODO: figure out why "stop" does not release the address
                        self.stop_servers()

                        sleep(1)

                        stop_count = 0
                        logger.critical(
                            "run@dns_server.py - Waiting for UDP Server to stop..."
                        )
                        while self.udp_server.thread and self.udp_server.isAlive():
                            if stop_count > 30:
                                logger.critical(
                                    "run@dns_server.py - UDP Server did not stop while reloading zones"
                                )
                                raise Exception(
                                    "run@dns_server.py - UDP Server threads went rogue during zone reload"
                                )
                            logger.info(
                                "run@dns_server.py - Waiting for DNS Server to stop before reloading zones"
                            )
                            stop_count = stop_count + 1
                            sleep(1)
                        stop_count = 0
                        logger.critical(
                            "run@dns_server.py - Waiting for TCP Server to stop..."
                        )
                        while self.tcp_server.thread and self.tcp_server.isAlive():
                            if stop_count > 30:
                                logger.critical(
                                    "run@dns_server.py - TCP Server did not stop while reloading zones"
                                )
                                raise Exception(
                                    "run@dns_server.py - TCP Server threads went rogue during zone reload"
                                )
                            logger.info(
                                "run@dns_server.py - Waiting for DNS Server to stop before reloading zones"
                            )
                            stop_count = stop_count + 1
                            sleep(1)
                        logger.critical(
                            "run@dns_server.py - Rebooting server with fresh zones..."
                        )
                        self.boot()
                        self.start_servers()

                count = count + 1
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

    def boot(self):
        port = self.get_port()
        listen = self.get_listen()

        self.resolver = Resolver(self.api_client)
        self.udp_server = DNSServer(
            self.resolver,
            address=listen,
            port=port,
            handler=DNSHandler,
            logger=DNSLogger(self.api_client),
        )
        self.tcp_server = DNSServer(
            self.resolver,
            address=listen,
            port=port,
            tcp=True,
            handler=DNSHandler,
            logger=DNSLogger(self.api_client),
        )

        logger.info("starting DNS server on port %d", port)

    def start_servers(self):
        self.udp_server.start_thread()
        self.tcp_server.start_thread()

    def stop_servers(self):
        self.udp_server.stop()
        self.udp_server.server.socket.close()
        self.udp_server.server.server_close()
        self.tcp_server.stop()
        self.tcp_server.server.socket.close()
        self.tcp_server.server.server_close()

