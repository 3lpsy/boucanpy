from ipaddress import ip_address
from bountydns.core.utils import load_env
from bountydns.core.security import hash_password
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.user import User


class UserCreate(BaseCommand):
    name = "user-create"
    aliases = ["user"]
    description = "create users via DB"

    @classmethod
    def parser(cls, parser):
        parser.add_argument(
            "-e",
            "--email",
            action="store",
            required=True,
            type=str,
            help="email address",
        )
        parser.add_argument(
            "-i",
            "--insecure-password",
            action="store",
            type=str,
            help="insecure password (use prompt or stdin)",
        )
        parser.add_argument(
            "-s", "--superuser", action="store_true", help="is superuser"
        )
        return parser

    async def run(self):
        self.load_env("api")
        self.db_register()
        email = self.option("email")
        password = self.get_password()
        hashed_password = hash_password(password)
        is_superuser = bool(self.option("superuser"))
        user = User(
            email=email, hashed_password=hashed_password, is_superuser=is_superuser
        )

        self.session().add(user)
        self.session().commit()

    def get_password(self):
        if self.option("insecure_password"):
            return self.option("insecure_password")
        raise NotImplementedError()
