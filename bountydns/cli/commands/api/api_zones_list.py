from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.zone import Zone


class ApiZonesList(BaseCommand):
    name = "apizoneslist"
    aliases = ["apizones"]
    description = "list zones via API"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        self.load_env("db")
        self.db_register("api")
        for zone in self.session("api").query(Zone).all():
            print(zone.id, zone.domain, zone.ip)
