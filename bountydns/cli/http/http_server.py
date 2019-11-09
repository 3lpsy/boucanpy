import os
from pathlib import Path
from time import sleep
from bountydns.core import logger
from bountydns.cli.base import BaseCommand
from bountydns.dns.api_client import ApiClient
from bountydns.http.manager import HttpServerManager


class HttpServer(BaseCommand):
    name = "http-server"
    aliases = ["http"]
    description = "run http server"
    add_log_level = True
    add_debug = True

    def __init__(self, *args, **kwargs):
        self.api_client = None
        self.http_server = None
        self.https_server = None
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
            "-p",
            "--port",
            action="store",
            type=int,
            default=80,
            help="listen port of the http server",
        )

        parser.add_argument(
            "-l",
            "--listen",
            action="store",
            default="127.0.0.1",
            help="bind address of the http server",
        )

        parser.add_argument(
            "-s", "--enable-ssl", action="store_true", help="enable the ssl server"
        )

        parser.add_argument(
            "--ssl-port",
            action="store",
            type=int,
            default=443,
            help="listen port of the https server",
        )

        parser.add_argument(
            "--ssl-listen",
            action="store",
            default="127.0.0.1",
            help="bind address of the https server",
        )

        # also need cert/pem paths

        parser.add_argument(
            "--no-sync",
            action="store_true",
            help="don't sync api token back to database",
        )

        parser.add_argument(
            "--no-api-wait", action="store_true", help="don't wait for the api to be up"
        )

        parser.add_argument(
            "--no-ssl-verify",
            action="store_true",
            help="skip ssl verify in the http server's api client",
        )

        parser.add_argument(
            "-r",
            "--refresh-ttl",
            type=int,
            default=3600,
            action="store",
            help="time to wait before polling for new things",
        )
        return parser

    async def run(self):

        # TODO: thread issues?
        verify_ssl = True
        if bool(self.option("no_ssl_verify")):
            verify_ssl = False

        self.api_client = ApiClient(
            self.get_api_url(), self.get_api_token(), verify_ssl=verify_ssl
        )

        if not self.option("no_api_wait"):
            if not self.api_client.wait_for_up():
                logger.critical(
                    "run@http_server.py - Could not connect to api. quitting"
                )
                self.exit(1)

        if self.option("no_sync"):
            logger.info("run@http_server.py - Skipping syncing api token")
        else:
            self.api_client.sync()

        self.boot()

        self.start_servers()

        try:
            count = 0
            while self.is_alive():
                # logger.info("run@http_server.py - Polling")
                #  if count > 0 and count % self.option("refresh_ttl") == 0:
                # if self.api_client.refresh_zones_if_needed():
                #     logger.critical(
                #         "run@dns_server.py - API Client found new or changed zones. Stopping servers..."
                #     )
                #     # TODO: figure out why "stop" does not release the address
                #     self.stop_servers()

                #     sleep(1)

                #     stop_count = 0
                #     logger.critical(
                #         "run@dns_server.py - Waiting for UDP Server to stop..."
                #     )
                #     while self.udp_server.thread and self.udp_server.isAlive():
                #         if stop_count > 30:
                #             logger.critical(
                #                 "run@dns_server.py - UDP Server did not stop while reloading zones"
                #             )
                #             raise Exception(
                #                 "run@dns_server.py - UDP Server threads went rogue during zone reload"
                #             )
                #         logger.info(
                #             "run@dns_server.py - Waiting for DNS Server to stop before reloading zones"
                #         )
                #         stop_count = stop_count + 1
                #         sleep(1)
                #     stop_count = 0
                #     logger.critical(
                #         "run@dns_server.py - Waiting for TCP Server to stop..."
                #     )
                #     while self.tcp_server.thread and self.tcp_server.isAlive():
                #         if stop_count > 30:
                #             logger.critical(
                #                 "run@dns_server.py - TCP Server did not stop while reloading zones"
                #             )
                #             raise Exception(
                #                 "run@dns_server.py - TCP Server threads went rogue during zone reload"
                #             )
                #         logger.info(
                #             "run@dns_server.py - Waiting for DNS Server to stop before reloading zones"
                #         )
                #         stop_count = stop_count + 1
                #         sleep(1)
                #     logger.critical(
                #         "run@dns_server.py - Rebooting server with fresh zones..."
                #     )
                #     self.boot()
                #     self.start_servers()

                count = count + 1
                sleep(1)

        except KeyboardInterrupt:
            pass

    def boot(self):
        port = self.option("port")
        listen = self.option("listen")

        self.http_server = HttpServerManager(
            port=port, listen=listen, ssl=False, api_client=self.api_client
        )

        logger.info("boot@http_server.py - Building http server on port %d", port)

        if bool(self.option("enable_ssl")):
            ssl_port = self.option("port")
            ssl_listen = self.option("listen")
            self.https_server = HttpServerManager(
                port=ssl_port, listen=ssl_listen, ssl=True, api_client=self.api_client
            )
            logger.info(
                "boot@http_server.py - Building https server on port %d", ssl_port
            )

    def start_servers(self):
        self.http_server.start_thread()
        if bool(self.option("enable_ssl")):
            self.https_server.start_thread()

    def stop_servers(self):
        self.http_server.stop()
        if bool(self.option("enable_ssl")):
            self.https_server.stop()

    def is_alive(self):
        _is_alive = self.http_server.is_alive()
        if bool(self.option("enable_ssl")):
            _is_alive = _is_alive and self.https_server.stop()

        return _is_alive

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
