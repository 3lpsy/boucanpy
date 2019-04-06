import jwt
from time import sleep
import requests
from dnslib import QTYPE, RCODE, RR

from bountydns.core.logger import logger

from bountydns.core.entities.zone.data import ZoneData


class ApiClient:
    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.api_token = api_token
        payload = jwt.decode(api_token, verify=False)  # do not trust
        if not "dns_server_name" in payload.keys() or not payload["dns_server_name"]:
            print("DNS SERVER PAYLOAD", payload)
            logger.critical("no dns_server_name on api token")
            raise Exception("no dns_server_name on api token")
        self.dns_server_name = payload["dns_server_name"]

    def wait_for_up(self):
        seconds = 0
        while True:
            if seconds > 60:
                logger.warning("could not connect to api. api not up")
                return False
            logger.info("checking for api status")
            try:
                # sleep(15)
                self.get_status()
                return True
            except Exception as e:
                logger.info(
                    "api check not ready after {} seconds: {}".format(
                        str(seconds), str(e.__class__.__name__)
                    )
                )
            seconds = seconds + 1
            sleep(1)

    def url(self, url):
        return self.api_url + "/api/v1" + url

    def get(self, url, fail=True):
        headers = self.get_default_headers()
        res = requests.get(self.url(url), headers=headers)
        if fail:
            res.raise_for_status()
        return res.json()

    def post(self, url, data=None, fail=True):
        data = data or {}
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

    def sync_api_token(self):
        logger.info("syncing api token")
        return self.post("/api-token/sync", fail=False)

    def get_status(self):
        return self.get("/status")

    def get_zones(self):
        logger.info("getting zones")

        dm = ZoneData
        zone_data = self.get(f"/dns-server/{self.dns_server_name}/zone")
        return [dm(**z) for z in zone_data["zones"]]

    def create_dns_request(self, handler, request, request_uuid):
        logger.info("creating dns request")

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
