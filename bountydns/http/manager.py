import threading
from bountydns.core import logger

from bountydns.http.handler import HttpHandler
from bountydns.http.server import HttpServer, HttpsServer


class HttpServerManager:
    def __init__(self, port=80, listen="127.0.0.1", ssl=False, api_client=None):
        self.port = int(port)
        self.listen = listen
        self.ssl = ssl
        self.api_client = api_client
        self.logger = logger
        if ssl:
            self.server = HttpServer(
                (self.listen, self.port), HttpHandler, api_client, logger
            )
        else:
            self.server = HttpsServer(
                (self.listen, self.port), HttpHandler, api_client, logger
            )

        self.thread = None

    def start(self):
        logger.info("start@server.py - Starting Http server")
        if not self.server:
            raise Exception("No server on HttpServer")
        self.server.serve_forever()

    def start_thread(self):
        proto = "https://" if self.ssl else "http://"
        logger.info(
            f"start_thread@server.py - Starting Http server thread for server: {proto}{self.listen}:{self.port}"
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        logger.info("stop@server.py - Stopping Http server")
        if not self.server:
            raise Exception("No server on HttpServer")
        self.server.shutdown()

    def is_alive(self):
        logger.info("is_alive@server.py - Checking if Http server is alive")
        if not self.thread:
            return False
        return self.thread.isAlive()

    # base method to control class initialization
    # process_request calls this first
    # def finish_request(self, request, client_address):
    #     """Finish one request by instantiating RequestHandlerClass."""
    #     self.RequestHandlerClass(request, client_address, self)
