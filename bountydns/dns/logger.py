from dnslib.server import DNSLogger as BaseDNSLogger


class DNSLogger(BaseDNSLogger):
    def __init__(self, api_client, log="request,reply", prefix=True):
        self.api = api_client
        super().__init__(log, prefix)

    def log_pass(self, *args):
        print("log_pass")

    def log_request(self, handler, request, request_uuid):
        print("log_request")
        self.api.create_dns_request(handler, request, request_uuid)
        super().log_request(handler, request)

    def log_reply(self, handler, reply, request_uuid):
        # zone may be none
        super().log_reply(handler, reply)
