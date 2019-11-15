import requests
from boucanpy.cli.base import BaseCommand
from boucanpy.db.models.user import User


class ApiUsersList(BaseCommand):
    name = "api-user-list"
    aliases = ["api-users"]
    description = "list users via API"
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
            "-t", "--auth-token", action="store", type=str, help="api token"
        )
        return parser

    async def run(self):
        res = requests.get(self.get_url(), headers=self.get_headers())
        print(res.json())

    def get_url(self):
        return self.option("api_url") + self.path

    def get_headers(self):
        return {"Authorization": "Bearer " + self.option("auth_token")}
