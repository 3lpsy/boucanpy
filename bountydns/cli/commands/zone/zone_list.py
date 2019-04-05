from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.zone import Zone


class ZoneList(BaseCommand):
    name = "zone-list"
    aliases = ["zones"]
    description = "list zones via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        for zone in self.session().query(Zone).all():
            print(zone.id, zone.domain, zone.ip, zone.dns_server_name)
