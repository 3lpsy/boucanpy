import threading
from bountydns.core import logger

from bountydns.http.handler import HttpHandler
from bountydns.http.server import HttpServer, HttpsServer
import ssl as ssllib


class HttpServerManager:
    def __init__(
        self,
        port=80,
        listen="127.0.0.1",
        ssl=False,
        ssl_key_path=None,
        ssl_cert_path=None,
        api_client=None,
    ):
        self.port = int(port)
        self.listen = listen
        self.ssl = ssl
        self.api_client = api_client
        self.logger = logger
        if not ssl:
            self.server = HttpServer(
                (self.listen, self.port), HttpHandler, api_client, logger
            )
        else:
            self.server = HttpsServer(
                (self.listen, self.port), HttpHandler, api_client, logger
            )
            logger.info(
                f"__init__@manager.py - Building ssl server with certfile: {ssl_cert_path} and keyfile: {ssl_key_path}"
            )
            self.server.socket = ssllib.wrap_socket(
                self.server.socket,
                server_side=True,
                certfile=ssl_cert_path,
                keyfile=ssl_key_path,
                ssl_version=ssllib.PROTOCOL_TLS,
            )

        self.thread = None

    def start(self):
        if self.ssl:
            logger.info("start@manager.py - Starting Https server")
        else:
            logger.info("start@manager.py - Starting Http server")
        if not self.server:
            raise Exception("No server on HttpServer")
        self.server.serve_forever()

    def start_thread(self):
        proto = "https://" if self.ssl else "http://"
        logger.info(
            f"start_thread@manager.py - Starting Http server thread for server: {proto}{self.listen}:{self.port}"
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        logger.info("stop@manager.py - Stopping Http server")
        if not self.server:
            raise Exception("No server on HttpServer")
        self.server.shutdown()

    def is_alive(self):
        if not self.thread:
            logger.info(
                "is_alive@manager.py -  HttpServer is not alive because there is not thread"
            )
            return False
        return self.thread.isAlive()

    # base method to control class initialization
    # process_request calls this first
    # def finish_request(self, request, client_address):
    #     """Finish one request by instantiating RequestHandlerClass."""
    #     self.RequestHandlerClass(request, client_address, self)
