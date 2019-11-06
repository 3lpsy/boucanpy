from dnslib.server import DNSLogger as BaseDNSLogger
from bountydns.core import logger


class DNSLogger(BaseDNSLogger):
    def __init__(self, api_client, log="request,reply", prefix=True):
        self.api = api_client
        super().__init__(log, prefix)

    def log_pass(self, *args):
        pass

    def log_request(self, handler, request, request_uuid):
        logger.debug(f"log_request: {handler}, {request}, {request_uuid}")
        self.api.create_dns_request(handler, request, request_uuid)
        super().log_request(handler, request)

    def log_reply(self, handler, reply, request_uuid):
        # zone may be none
        super().log_reply(handler, reply)
