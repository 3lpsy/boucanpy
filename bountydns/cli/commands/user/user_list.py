from bountydns.core.utils import load_env
from bountydns.cli.commands.base import BaseCommand
from bountydns.db.models.user import User


class UserList(BaseCommand):
    name = "user-list"
    aliases = ["users"]
    description = "list users via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    def run(self):
        self.load_env("db")
        self.db_register("api")
        for user in self.session("api").query(User).all():
            print(user.id, user.email, user.is_superuser)
