import requests
import binascii, time
from dnslib import QTYPE, RCODE, RR
from bountydns.core import logger


class DnsLogger:
    def __init__(self, api_url, api_token, prefix=""):
        self.api_url = api_url
        self.api_token = api_token
        self.prefix = prefix

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        if self.prefix:
            return "%s [%s:%s] " % (
                time.strftime("%Y-%m-%d %X"),
                handler.__class__.__name__,
                handler.server.resolver.__class__.__name__,
            )
        else:
            return ""

    def log_recv(self, handler, data):
        logger.debug(
            "%sReceived: [%s:%d] (%s) <%d> : %s"
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                len(data),
                binascii.hexlify(data),
            )
        )

    def log_send(self, handler, data):
        logger.debug(
            "%sSent: [%s:%d] (%s) <%d> : %s"
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                len(data),
                binascii.hexlify(data),
            )
        )

    def log_request(self, handler, request):
        url = self.api_url + "/api/v1/dns-request"
        data = {
            "name": str(request.q.qname),
            "source_address": str(handler.client_address[0]),
            "source_port": int(handler.client_address[1]),
            "type": str(QTYPE[request.q.qtype]),
            "protocol": str(handler.protocol),
        }
        res = requests.post(
            url,
            headers={"Authorization": "Bearer {}".format(self.api_token)},
            json=data,
        )
        print(res.status_code)

        print(res.json())

        logger.info(
            "%sRequest: [%s:%d] (%s) / '%s' (%s)"
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                request.q.qname,
                QTYPE[request.q.qtype],
            )
        )
        self.log_data(request)

    def log_reply(self, handler, reply):
        if reply.header.rcode == RCODE.NOERROR:
            logger.info(
                "%sReply: [%s:%d] (%s) / '%s' (%s) / RRs: %s"
                % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr]),
                )
            )
        else:
            logger.info(
                "%sReply: [%s:%d] (%s) / '%s' (%s) / %s"
                % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    RCODE[reply.header.rcode],
                )
            )
        self.log_data(reply)

    def log_truncated(self, handler, reply):
        logger.debug(
            "%sTruncated Reply: [%s:%d] (%s) / '%s' (%s) / RRs: %s"
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                reply.q.qname,
                QTYPE[reply.q.qtype],
                ",".join([QTYPE[a.rtype] for a in reply.rr]),
            )
        )
        self.log_data(reply)

    def log_error(self, handler, e):
        logger.debug(
            "%sInvalid Request: [%s:%d] (%s) :: %s"
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                e,
            )
        )

    def log_data(self, dnsobj):
        logger.debug(str(dnsobj.toZone("    ")))
