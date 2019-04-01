import requests
from bountydns.cli.commands.base import BaseCommand


class ApiZoneCreate(BaseCommand):
    name = "api-zone-create"
    aliases = ["api-zone"]
    description = "create user via API"
    path = "/api/v1/user"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-a",
            "--api-url",
            action="store",
            type=str,
            default="http://127.0.0.1:8080",
            help="api address",
        )
        parser.add_argument(
            "-t",
            "--auth-token",
            action="store",
            type=str,
            required=True,
            help="api token",
        )
        parser.add_argument(
            "-d",
            "--domain",
            action="store",
            required=True,
            type=str,
            help="zone domain",
        )
        parser.add_argument(
            "-i",
            "--ip-address",
            action="store",
            type=str,
            required=True,
            help="resolvable ip",
        )
        return parser

    def run(self):
        # TODO: run this
        url = self.option("api_url")
        domain = self.option("domain")
        ip = self.option("ip_addresss")
        print(f"attempting to create zone {self.get_url()}")
        # spec requires form-data
        response = requests.post(
            self.get_url(),
            headers={"Authorization": "Bearer {}".format(self.option("auth_token"))},
            json={"domain": domain, "ip": ip},
        )
        json_res = response.json()
        print(json_res)

    def get_url(self):
        return self.option("api_url") + self.path
