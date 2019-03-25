import requests
from bountydns.cli.commands.base import BaseCommand


class ApiLogin(BaseCommand):
    name = "api-login"
    aliases = ["zones"]
    description = "login via API"

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

    def run(self):
        url = self.option("api_url")
        email = self.option("email")
        password = self.get_password()
        print(f"attempting to login to {self.get_url()}")
        response = requests.post(self.get_url(), json=self.get_json())
        json_res = response.json()
        print(json_res)

    def get_url(self):
        return self.option("api_url") + "/api/v1/auth/login"

    def get_json(self):
        return {"username": self.option("email"), "password": self.get_password()}

    def get_password(self):
        if self.option("insecure_password"):
            return self.option("insecure_password")
        raise NotImplementedError()
