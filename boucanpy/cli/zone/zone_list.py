from boucanpy.cli.base import BaseCommand
from boucanpy.db.models.zone import Zone


class ZoneList(BaseCommand):
    name = "zone-list"
    aliases = ["zones"]
    description = "list zones via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        self.db_register()
        for zone in self.session().query(Zone).all():
            print(zone.id, zone.domain, zone.ip, zone.dns_server.name)
