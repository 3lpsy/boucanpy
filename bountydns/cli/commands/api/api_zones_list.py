from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.zone import Zone


class ApiZonesList(BaseCommand):
    name = "api-zone-list"
    aliases = ["api-zones"]
    description = "list zones via API"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-a",
            "--api-url",
            action="store",
            type=str,
            default="http://127.0.0.1:8000",
            help="api address",
        )
        parser.add_argument("-t", "--token", action="store", type=str, help="api token")
        return parser

    def run(self):
        pass
