import requests
import binascii, time
from dnslib import QTYPE, RCODE, RR
from dnslib.server import DNSLogger as BaseDNSLogger
from bountydns.core import logger


class DNSLogger(BaseDNSLogger):
    def __init__(self, api_client, log="", prefix=True):
        self.api = api_client
        super().__init__(log, prefix)

    def log_recv(self, handler, request, request_uuid):
        super().log_recv(handler, request)
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

    def log_send(self, handler, reply, request_uuid):
        super().log_send(handler, request)
