from datetime import timedelta, datetime

import uuid
from boucanpy.core.enums import NODE_SCOPES
from boucanpy.core.security import create_bearer_token
from boucanpy.core.api_token import ApiTokenRepo
from boucanpy.cli.base import BaseCommand
from boucanpy.db.models.api_token import ApiToken


class ApiTokenCreate(BaseCommand):
    name = "api-token-create"
    aliases = ["token"]
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
            "--server-name",
            action="store",
            type=str,
            help="dns/http server name (aaa-bbb-ccc)",
        )

        return parser

    async def run(self):
        self.db_register()

        server_name = self.option("server_name", None) or uuid.uuid4().hex

        scopes = self.get_scopes()
        expires_delta = timedelta(days=int(self.option("days")))
        expires_at = datetime.utcnow() + expires_delta

        token = create_bearer_token(
            data={
                "sub": self.option("user_id"),
                "scopes": scopes,
                "dns_server_name": server_name,
                "http_server_name": server_name,
            },
            expire=expires_at,
        )

        print("API_TOKEN:{}".format(str(token)))

    def get_scopes(self):
        if self.option("scope"):
            return " ".join(self.option("scope"))
        else:
            return NODE_SCOPES
