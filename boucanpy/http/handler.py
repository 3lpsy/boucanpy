import socket  # for timeout
from http.server import BaseHTTPRequestHandler
import io
import os
import shutil

# use self.server to get api_client and logger

# three important things are: vhost(domain/zone), path, and method/request type


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.logger.info("do_GET@handler.py - Handling request")
        self.create_http_request("GET")
        return self.dummy_response()

    def do_HEAD(self):
        self.server.logger.info("do_HEAD@handler.py - Handling request")
        self.create_http_request("HEAD")
        return self.dummy_response()

    def do_OPTIONS(self):
        self.server.logger.info("do_OPTIONS@handler.py - Handling request")

        self.create_http_request("OPTIONS")
        return self.dummy_response()

    def do_POST(self):
        self.server.logger.info("do_POST@handler.py - Handling request")
        self.create_http_request("POST")
        return self.dummy_response()

    def do_PATCH(self):
        self.server.logger.info("do_PATCH@handler.py - Handling request")
        self.create_http_request("PATCH")
        return self.dummy_response()

    def do_PUT(self):
        self.server.logger.info("do_PUT@handler.py - Handling request")
        self.create_http_request("PUT")
        return self.dummy_response()

    def do_DELETE(self):
        self.server.logger.info("do_DELETE@handler.py - Handling request")
        self.create_http_request("DELETE")
        return self.dummy_response()

    def send_error(self, code, message=None, explain=None):
        self.server.logger.info("send_error@handler.py - Sending error")

        type = "ERROR"
        if hasattr(self, "headers"):
            name = self.headers.get("HOST", self.client_address[0])
        else:
            name = self.client_address[0]

        if ":" in name:
            name = name.split(":")[0]

        path = self.path or "UNKNOWN"

        source_address = self.client_address[0]
        source_port = self.client_address[1]
        protocol = self.get_protocol()
        raw_request = (
            "ERROR: "
            + str(code)
            + "\n"
            + "MESSAGE: "
            + str(message)
            + "\n"
            + "EXPLAIN: "
            + str(explain)
        )
        self.server.api_client.create_http_request(
            name, path, source_address, source_port, type, protocol, raw_request,
        )
        return super().send_error(code, message=None, explain=None)

    def dummy_response(self):

        f = io.BytesIO()
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title></title>\n")
        f.write(b"<body>\n")
        f.write(b"<h2>Message: Found</h2>\n")
        f.write(b"</body>\n")
        f.write(b"</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def create_http_request(self, method):
        self.server.logger.info(
            "create_http_request@handler.py - Creating HTTP request"
        )
        type = method.upper()
        if hasattr(self, "headers"):
            name = self.headers.get("HOST", self.client_address[0])
        else:
            name = self.client_address[0]

        path = self.path

        if ":" in name:
            name = name.split(":")[0]
        source_address = self.client_address[0]
        source_port = self.client_address[1]
        protocol = self.get_protocol()
        raw_request = str(self.build_raw_request(method))
        self.server.api_client.create_http_request(
            name, path, source_address, source_port, type, protocol, raw_request,
        )

    def build_raw_request(self, method):
        self.server.logger.info("build_raw_request@handler.py - Building Raw Request")
        request = self.raw_requestline.decode().rstrip("\n\r")

        self.server.logger.info(
            "build_raw_request@handler.py - Attaching headers to Raw Request"
        )

        if hasattr(self, "headers"):
            for h, v in self.headers.items():
                request = request + "\n" + str(h) + ": " + str(v)

        if method in ["PUT", "POST", "PATCH", "DELETE"]:
            self.server.logger.info(
                "build_raw_request@handler.py - Parsing data for Raw Request"
            )
            data = self.parse_data()
            try:
                data = data.decode()
            except Exception as e:
                self.server.logger.warning(
                    "build_raw_request@handler.py - Error decoding data."
                )
            request = request + "\n\n" + str(data)
        return request

    def parse_data(self):
        content_length = 0
        try:
            found = False
            for h, v in self.headers.items():
                if h.lower() == "content-length":
                    content_length = int(v)
                    found = True
            if not found:
                self.server.logger.warning(
                    "parse_data@handler.py - No Content-Length found on request."
                )
                # this is where it fails, because i cannot read data without hanging unless I know how much data to read
        except Exception as e:
            self.server.logger.warning(
                "parse_data@handler.py - Error Reading Content-Length from request."
            )
            data = "".encode()
            return data

        try:
            data = self.rfile.read(content_length)
            return data
        except socket.timeout as e:
            # a read or a write timed out.
            self.server.logger.warning(
                f"parse_data@handler.py - Timeout reading data {content_length}"
            )
            # data = "".encode()
            return data

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def get_protocol(self):
        return "https" if self.server.is_ssl else "http"
