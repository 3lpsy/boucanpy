from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand


class ApiUrls(BaseCommand):
    name = "api-urls"
    aliases = ["urls"]
    description = "list api urls"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        load_env("api")
        load_env("api")
        from bountydns.api.main import api

        for route in api.routes:
            print(route.name, route.path, getattr(route, "methods", None))
