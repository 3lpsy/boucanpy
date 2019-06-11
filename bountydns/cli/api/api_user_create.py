import requests
from bountydns.cli.base import BaseCommand


class ApiUserCreate(BaseCommand):
    name = "api-user-create"
    aliases = ["api-user"]
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
            "-e",
            "--email",
            action="store",
            required=True,
            type=str,
            help="email address",
        )
        parser.add_argument(
            "-i",
            "--insecure-password",
            action="store",
            type=str,
            help="insecure password (use prompt or stdin)",
        )
        return parser

    async def run(self):
        url = self.option("api_url")
        email = self.option("email")
        password = self.get_password()
        print(f"attempting to create user {self.get_url()}")
        # spec requires form-data
        response = requests.post(
            self.get_url(),
            headers={"Authorization": "Bearer {}".format(self.option("auth_token"))},
            json=self.get_json(),
        )
        json_res = response.json()
        print(json_res)

    def get_url(self):
        return self.option("api_url") + self.path

    def get_json(self):
        return {
            "email": self.option("email"),
            "password": self.get_password(),
            "password_confirm": self.get_password(),
        }

    def get_password(self):
        if self.option("insecure_password"):
            return self.option("insecure_password")
        raise NotImplementedError()
