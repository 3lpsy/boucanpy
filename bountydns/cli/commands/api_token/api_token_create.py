from datetime import timedelta
import uuid
from bountydns.core.utils import load_env
from bountydns.core.security import create_bearer_token
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.api_token import ApiToken


class ApiTokenCreate(BaseCommand):
    name = "api-token-create"
    aliases = ["api-token"]
    description = "create api-tokens directly"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-u", "--user-id", action="store", default=1, type=str, help="user id (sub)"
        )
        parser.add_argument("-s", "--scope", action="append", type=str, help="scopes")
        parser.add_argument(
            "-m",
            "--minutes",
            action="store",
            default=3600,
            type=str,
            help="minutes valid for",
        )
        parser.add_argument(
            "-n",
            "--dns-server-name",
            action="store",
            type=str,
            help="dns server name (aaa-bbb-ccc)",
        )
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        expires_delta = timedelta(minutes=self.option("minutes"))
        dns_server_name = self.option("dns_server_name", None) or uuid.uuid4().hex
        token = create_bearer_token(
            data={
                "sub": self.option("user_id"),
                "scopes": self.get_scopes(),
                "dns_server_name": dns_server_name,
            },
            expires_delta=expires_delta,
        )
        print("API_TOKEN:{}".format(str(token.decode())))

    def get_scopes(self):
        if self.option("scope"):
            return " ".join(self.option("scope"))
        else:
            return "profile dns-request:create dns-request:list zone:list zone:read refresh"
