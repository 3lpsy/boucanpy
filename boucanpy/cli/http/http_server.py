import os
from pathlib import Path
from time import sleep
from boucanpy.core import logger
from boucanpy.core.utils import storage_dir
from boucanpy.cli.base import BaseCommand
from boucanpy.api_client import ApiClient
from boucanpy.http.manager import HttpServerManager


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

        parser.add_argument(
            "--ssl-key-path",
            action="store",
            default=storage_dir("ssl/devkey.pem"),
            help="path to ssl key",
        )

        parser.add_argument(
            "--ssl-cert-path",
            action="store",
            default=storage_dir("ssl/devcert.pem"),
            help="path to ssl cert",
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
                # zones don't need to be refreshed for http server
                # may want to do something in the future thought
                count = count + 1
                sleep(1)

        except KeyboardInterrupt:
            pass

    def boot(self):
        port = self.option("port")
        listen = self.option("listen")

        logger.info("boot@http_server.py - Building http server on port %d", port)

        self.http_server = HttpServerManager(
            port=port, listen=listen, ssl=False, api_client=self.api_client
        )

        if bool(self.option("enable_ssl")):

            ssl_port = self.option("ssl_port")
            ssl_listen = self.option("ssl_listen")
            ssl_key_path = self.option("ssl_key_path")
            ssl_cert_path = self.option("ssl_cert_path")
            logger.info(
                f"boot@http_server.py - Building https server manager on port {str(ssl_port)} with {ssl_cert_path} and {ssl_key_path}",
            )

            self.https_server = HttpServerManager(
                port=ssl_port,
                listen=ssl_listen,
                api_client=self.api_client,
                ssl=True,
                ssl_cert_path=ssl_cert_path,
                ssl_key_path=ssl_key_path,
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
            _is_alive = _is_alive and self.https_server.is_alive()

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
