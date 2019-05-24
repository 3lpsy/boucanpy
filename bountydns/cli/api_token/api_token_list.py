from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.api_token import ApiToken


class ApiTokenList(BaseCommand):
    name = "api-token-list"
    aliases = ["api-tokens"]
    description = "list api-tokens via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        for zone in self.session().query(ApiToken).all():
            print(zone.id, zone.scopes, zone.token)
