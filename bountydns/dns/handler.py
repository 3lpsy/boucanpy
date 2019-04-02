import struct, uuid
from dnslib.server import DNSHandler as BaseDNSHandler


class DNSHandler(BaseDNSHandler):
    def handle(self):
        if self.server.socket_type == socket.SOCK_STREAM:
            self.protocol = "tcp"
            data = self.request.recv(8192)
            length = struct.unpack("!H", bytes(data[:2]))[0]
            while len(data) - 2 < length:
                new_data = self.request.recv(8192)
                if not new_data:
                    break
                data += new_data
            data = data[2:]
        else:
            self.protocol = "udp"
            data, connection = self.request

        request_uuid = uuid.uuid4()
        self.server.logger.log_recv(self, data, request_uuid)

        try:
            rdata = self.get_reply(data)
            self.server.logger.log_send(self, rdata, request_uuid)

            if self.protocol == "tcp":
                rdata = struct.pack("!H", len(rdata)) + rdata
                self.request.sendall(rdata)
            else:
                connection.sendto(rdata, self.client_address)

        except DNSError as e:
            self.server.logger.log_error(self, e)
