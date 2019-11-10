import jwt

from time import sleep
import requests
from dnslib import QTYPE, RCODE, RR
from urllib3.exceptions import InsecureRequestWarning

from bountydns.core import logger

from bountydns.core.zone.data import ZoneData


class ApiClient:
    def __init__(self, api_url, api_token, verify_ssl=True):
        self.api_url = api_url
        self.api_token = api_token
        self.zones = []
        self.verify_ssl = verify_ssl
        if not self.verify_ssl:
            logger.warning(
                "__init__@dns_server.py - Disabling SSL Warnings. I hope this was intentional"
            )
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        payload = jwt.decode(api_token, verify=False)  # do not trust
        if not "dns_server_name" in payload.keys() or not payload["dns_server_name"]:
            logger.critical(
                f"__init__@api_client.py - No dns_server_name on api token payload: {str(payload)}"
            )
        self.dns_server_name = payload.get("dns_server_name", "")

        if not "http_server_name" in payload.keys() or not payload["http_server_name"]:
            logger.critical(
                f"__init__@api_client.py - No http_server_name on api token payload: {str(payload)}"
            )
        self.http_server_name = payload.get("http_server_name", "")

    def sync(self):
        logger.info("sync@api_client.py - Syncing api token")
        return self.post("/api-token/sync", fail=True)

    def get_zones(self):
        logger.info("get_zones@api_client.py - Getting zones")
        zone_data = self.get(
            f"/dns-server/{self.dns_server_name}/zone",
            params={"includes": ["dns_records"]},
        )
        data = [ZoneData(**z) for z in zone_data["zones"]]
        return data

    def load_zones(self):
        self.zones = self.get_zones()
        return True

    def refresh_zones_if_needed(self):
        logger.info(
            "refresh_zones_if_needed@api_client.py - Checking for New Zones and Records..."
        )
        old_zones = self.zones
        new_zones = self.get_zones()
        # TODO: fix this mess

        if len(old_zones) != len(new_zones):
            logger.warning(
                f"refresh_zones_if_needed@api_client.py - Zone Length mistmatch. New or Changed Zone Found: {str(old_zones)} != {str(new_zones)}. Reloading zones."
            )
            self.load_zones()
            return True

        for nz in new_zones:
            # make sure new zones are in old zones
            is_nz_exists = False
            for oz in old_zones:
                if oz.domain == nz.domain and oz.ip == nz.ip:
                    nz_dns_records = nz.dns_records or []
                    for nrec in nz_dns_records:
                        is_rec_satisfied = False
                        oz_dns_records = oz.dns_records or []
                        if len(nz_dns_records) != len(oz_dns_records):
                            logger.warning(
                                f"refresh_zones_if_needed@api_client.py - Zone Record Length mistmatch {str(len(nz_dns_records))} != {str(len(oz_dns_records))}. New or Changed Zone Record Found: {str(nz_dns_records)} != {str(oz_dns_records)}. Reloading zones."
                            )
                            self.load_zones()
                            return True
                        for orec in oz_dns_records:
                            if orec.record == nrec.record and orec.sort == nrec.sort:
                                is_rec_satisfied = True
                        if not is_rec_satisfied:
                            logger.warning(
                                f"refresh_zones_if_needed@api_client.py - New or Changed Zone Record {str(nz)}: {str(nrec)} found for server. Reloading zones."
                            )
                            self.load_zones()
                            return True
                    is_nz_exists = True
            if not is_nz_exists:
                logger.warning(
                    f"refresh_zones_if_needed@api_client.py - New or Changed Zone {str(nz)} found for server. Reloading zones."
                )
                self.load_zones()
                return True

        logger.info(
            "refresh_zones_if_needed@api_client.py - No New Zones or Records Found. All is well"
        )

        return False

    def get_status(self):
        return self.get("/status")

    def create_dns_request(self, handler, request, request_uuid):
        logger.info("create_dns_request@api_client.py - Creating dns request")

        name = str(request.q.qname)
        name = name.rstrip(".")
        data = {
            "name": name,
            "source_address": str(handler.client_address[0]),
            "source_port": int(handler.client_address[1]),
            "type": str(QTYPE[request.q.qtype]),
            "protocol": str(handler.protocol),
            "dns_server_name": str(self.dns_server_name),
            "raw_request": str(request),
        }
        self.post("/dns-request", data=data)

    def create_http_request(
        self, name, path, source_address, source_port, type, protocol, raw_request,
    ):
        logger.info("create_http_request@api_client.py - Creating http request")

        data = {
            "name": name,
            "path": path,
            "source_address": str(source_address),
            "source_port": int(source_port),
            "type": str(type),
            "protocol": str(protocol),
            "http_server_name": str(self.http_server_name),
            "raw_request": str(raw_request),
        }
        self.post("/http-request", data=data)

    def url(self, url):
        return self.api_url + "/api/v1" + url

    def get(self, url: str, params=None, fail=True):
        params = params or {}
        headers = self.get_default_headers()
        logger.info("get@api_client.py - Getting URL: " + str(self.url(url)))

        res = requests.get(
            self.url(url), headers=headers, params=params, verify=self.verify_ssl
        )

        if fail:
            if res.status_code != 200:
                logger.critical(
                    f"get@api_client.py - Error getting API {self.url(url)}: "
                    + str(res.json())
                )
            res.raise_for_status()
        return res.json()

    def post(self, url: str, data=None, fail=True):
        data = data or {}
        headers = self.get_default_headers()
        logger.info("post@api_client.py - Posting URL: " + str(self.url(url)))

        res = requests.post(
            self.url(url), json=data, headers=headers, verify=self.verify_ssl
        )

        if fail:
            if res.status_code != 200:
                logger.critical(
                    f"Error posting API {self.url(url)}: " + str(res.json())
                )
            res.raise_for_status()
        return res.json()

    def get_default_headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Accept": "application/json",
        }

    def wait_for_up(self):
        attempts = 0
        while True:
            if attempts > 60:
                logger.warning("could not connect to api. api not up")
                return False
            logger.info(
                f"wait_for_up@api_client.py - checking for api status : {self.url('/status')}"
            )
            try:
                sleep(1)
                self.get_status()
                sleep(3)
                return True
            except Exception as e:
                logger.info(
                    "wait_for_up@api_client.py - api check not ready after {} attempts: {}".format(
                        str(attempts), str(e.__class__.__name__)
                    )
                )
            attempts = attempts + 1
            sleep(1)
