from ipaddress import ip_address
from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.zone import Zone


class ZoneCreate(BaseCommand):
    name = "zone-create"
    aliases = ["zone"]
    description = "create zones via DB"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-i", "--ip", required=True, action="store", help="zone ip to resolve"
        )
        parser.add_argument(
            "-d", "--domain", required=True, action="store", help="zone root domain"
        )
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        ip = self.get_ip()
        domain = self.get_domain()
        zone = Zone(ip=ip, domain=domain)
        self.session().add(zone)
        self.session().commit()

    def get_ip(self):
        ip_raw = self.options.get("ip")
        try:
            ip_address(ip_raw)
        except ValueError as e:
            print("invalid ip address")
            print(e)
            self.exit(1)
        return ip_raw

    def get_domain(self):
        domain = self.option("domain")
        if "." not in domain:
            print("invalid domain")
            self.exit(1)
        return domain
