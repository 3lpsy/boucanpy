from bountydns.core.utils import load_env
from bountydns.cli.base import BaseCommand


class ApiUrls(BaseCommand):
    name = "api-urls"
    aliases = ["urls"]
    description = "list api urls"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        from bountydns.api.main import api

        for route in api.routes:
            print(route.name, route.path, getattr(route, "methods", None))
