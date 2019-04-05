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

    async def run(self):
        self.load_env("api")
        self.db_register()
        for user in self.session().query(User).all():
            print(user.id, user.email, user.is_superuser)
