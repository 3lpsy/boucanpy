import binascii,time
from dnslib import QTYPE,RCODE,RR
from bountydns.core import logger

class DnsLogger:

    def __init__(self, api_client=None, prefix=''):
        self.api_client = None

        if api_client and api_client.authenticate():
            self.api_client = api_client
        self.prefix = prefix

    def log_pass(self,*args):
        pass

    def log_prefix(self,handler):
        if self.prefix:
            return "%s [%s:%s] " % (time.strftime("%Y-%m-%d %X"),
                               handler.__class__.__name__,
                               handler.server.resolver.__class__.__name__)
        else:
            return ""

    def log_recv(self,handler,data):
        logger.debug("%sReceived: [%s:%d] (%s) <%d> : %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    len(data),
                    binascii.hexlify(data)))

    def log_send(self,handler,data):
        logger.debug("%sSent: [%s:%d] (%s) <%d> : %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    len(data),
                    binascii.hexlify(data)))

    def log_request(self,handler,request):
        if self.api_client:
            self.api_client.dns_event.make(
                event="REQUESTED",
                name=request.q.qname,
                type=QTYPE[request.q.qtype],
                source_address=handler.client_address[0],
                source_port=handler.client_address[1],
                protocol=handler.protocol
            )
        logger.info("%sRequest: [%s:%d] (%s) / '%s' (%s)" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    request.q.qname,
                    QTYPE[request.q.qtype]))
        self.log_data(request)

    def log_reply(self,handler,reply):
        if self.api_client:
            self.api_client.dns_event.make(
                event="REPLIED",
                name=reply.q.qname,
                type=QTYPE[reply.q.qtype],
                source_address=handler.client_address[0],
                source_port=handler.client_address[1],
                protocol=handler.protocol
            )
        if reply.header.rcode == RCODE.NOERROR:
            logger.info("%sReply: [%s:%d] (%s) / '%s' (%s) / RRs: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr])))
        else:
            logger.info("%sReply: [%s:%d] (%s) / '%s' (%s) / %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    RCODE[reply.header.rcode]))
        self.log_data(reply)

    def log_truncated(self,handler,reply):
        logger.debug("%sTruncated Reply: [%s:%d] (%s) / '%s' (%s) / RRs: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr])))
        self.log_data(reply)

    def log_error(self,handler,e):
        logger.debug("%sInvalid Request: [%s:%d] (%s) :: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    e))

    def log_data(self,dnsobj):
        logger.debug(str(dnsobj.toZone("    ")))