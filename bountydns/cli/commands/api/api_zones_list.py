import requests
from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.zone import Zone


class ApiZonesList(BaseCommand):
    name = "api-zone-list"
    aliases = ["api-zones"]
    description = "list zones via API"
    path = "/api/v1/zone"

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
            "-t", "--auth-token", action="store", type=str, help="api token"
        )
        return parser

    def run(self):
        res = requests.get(self.get_url(), headers=self.get_headers())
        print(res.json())

    def get_url(self):
        return self.option("api_url") + self.path

    def get_headers(self):
        return {"Authorization": "Bearer " + self.option("auth_token")}
