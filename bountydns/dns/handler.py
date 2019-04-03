import struct, uuid, socket
from dnslib.server import DNSHandler as BaseDNSHandler
from dnslib import DNSRecord, DNSError, QTYPE, RCODE, RR


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

        self.server.logger.log_recv(self, data)

        try:
            request_uuid = uuid.uuid4()
            rdata, zone = self.get_reply(data, request_uuid)
            self.server.logger.log_send(self, rdata, zone, request_uuid)

            if self.protocol == "tcp":
                rdata = struct.pack("!H", len(rdata)) + rdata
                self.request.sendall(rdata)
            else:
                connection.sendto(rdata, self.client_address)

        except DNSError as e:
            self.server.logger.log_error(self, e)

    def get_reply(self, data, request_uuid):
        request = DNSRecord.parse(data)
        self.server.logger.log_request(self, request, request_uuid)

        resolver = self.server.resolver
        reply, zone = resolver.resolve(request, self)
        self.server.logger.log_reply(self, reply)

        if self.protocol == "udp":
            rdata = reply.pack()
            if self.udplen and len(rdata) > self.udplen:
                truncated_reply = reply.truncate()
                rdata = truncated_reply.pack()
                self.server.logger.log_truncated(self, truncated_reply)
        else:
            rdata = reply.pack()

        return rdata, zone
