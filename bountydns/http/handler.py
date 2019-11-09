from http.server import BaseHTTPRequestHandler


# use self.server to get api_clietn and logger

# three important things are: vhost(domain/zone), path, and method/request type


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(type(self.server))
        self.server.logger.info("do_GET@handler.py - Handling request")
        return self.dummy_response()

    def do_HEAD(self):
        print(type(self.server))
        self.server.logger.info("do_HEAD@handler.py - Handling request")
        return self.dummy_response()

    def do_OPTIONS(self):
        print(type(self.server))
        self.server.logger.info("do_OPTIONS@handler.py - Handling request")
        return self.dummy_response()

    def do_POST(self):
        print(type(self.server))
        self.server.logger.info("do_POST@handler.py - Handling request")
        return self.dummy_response()

    def do_PATCH(self):
        print(type(self.server))
        self.server.logger.info("do_PATCH@handler.py - Handling request")
        return self.dummy_response()

    def do_PUT(self):
        print(type(self.server))
        self.server.logger.info("do_PUT@handler.py - Handling request")
        return self.dummy_response()

    def do_DELETE(self):
        print(type(self.server))
        self.server.logger.info("do_DELETE@handler.py - Handling request")
        return self.dummy_response()

    def do_OPTIONS(self):
        print(type(self.server))
        self.server.logger.info("do_OPTIONS@handler.py - Handling request")
        return self.dummy_response()

    def send_error(self, code, message=None, explain=None):
        self.server.logger.info("send_error@handler.py - Sending error")
        return super().send_error(code, message=None, explain=None)

    def dummy_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        return ""
