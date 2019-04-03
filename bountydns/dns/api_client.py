import jwt
import requests
from dnslib import QTYPE, RCODE, RR

from bountydns.core.entities.zone.data import ZoneData


class ApiClient:
    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.api_token = api_token
        payload = jwt.decode(api_token, verify=False)  # do not trust
        self.dns_server_name = payload["dns_server_name"]

    def url(self, url):
        return self.api_url + "/api/v1" + url

    def get(self, url, fail=True):
        headers = self.get_default_headers()
        res = requests.get(self.url(url), headers=headers)
        if fail:
            res.raise_for_status()
        return res.json()

    def post(self, url, data, fail=True):
        headers = self.get_default_headers()
        res = requests.post(self.url(url), json=data, headers=headers)
        if fail:
            res.raise_for_status()
        return res.json()

    def get_default_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Accept": "application/json",
        }

    def get_zones(self):
        dm = ZoneData
        zone_data = self.get(f"/dns-server/{self.dns_server_name}/zone")
        return [dm(**z) for z in zone_data["zones"]]

    def create_dns_request(self, handler, request, request_uuid):
        name = str(request.q.qname)
        name = name.rstrip(".")
        data = {
            "name": name,
            "source_address": str(handler.client_address[0]),
            "source_port": int(handler.client_address[1]),
            "type": str(QTYPE[request.q.qtype]),
            "protocol": str(handler.protocol),
            "dns_server_name": str(self.dns_server_name),
        }
        self.post("/dns-request", data=data)
