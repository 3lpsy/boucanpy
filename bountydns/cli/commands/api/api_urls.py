from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand


class ApiUrls(BaseCommand):
    name = "apiurls"
    aliases = ["urls"]
    description = "list api urls"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        load_env("db")
        load_env("api")
        from bountydns.api.main import api

        for route in api.routes:
            print(route.name, route.path, route.methods)
