from datetime import timedelta, datetime

import uuid
from bountydns.core.utils import load_env
from bountydns.core.security import create_bearer_token
from bountydns.core.entities import ApiTokenRepo
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
            "-d", "--days", action="store", default=30, type=str, help="days valid for"
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
        dns_server_name = self.option("dns_server_name", None) or uuid.uuid4().hex
        scopes = self.get_scopes()
        expires_delta = timedelta(days=self.option("days"))
        expires_at = datetime.utcnow() + expires_delta

        token = create_bearer_token(
            data={
                "sub": self.option("user_id"),
                "scopes": scopes,
                "dns_server_name": dns_server_name,
            },
            expire=expires_at,
        )

        print("API_TOKEN:{}".format(str(token.decode())))

    def get_scopes(self):
        if self.option("scope"):
            return " ".join(self.option("scope"))
        else:
            return "profile dns-request:create dns-request:list zone:list zone:read refresh api-token:syncable"
