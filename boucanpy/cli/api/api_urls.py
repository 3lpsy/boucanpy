from boucanpy.cli.base import BaseCommand


class ApiUrls(BaseCommand):
    name = "api-urls"
    aliases = ["urls"]
    description = "list api urls"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        from boucanpy.api.main import api

        for route in api.routes:
            print(route.name, route.path, getattr(route, "methods", None))
