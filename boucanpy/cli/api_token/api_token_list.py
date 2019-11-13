from boucanpy.core.utils import load_env
from boucanpy.cli.base import BaseCommand
from boucanpy.db.models.api_token import ApiToken


class ApiTokenList(BaseCommand):
    name = "api-token-list"
    aliases = ["api-tokens"]
    description = "list api-tokens via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        self.db_register()
        for zone in self.session().query(ApiToken).all():
            print(zone.id, zone.scopes, zone.token)
