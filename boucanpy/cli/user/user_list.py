from boucanpy.core.utils import load_env
from boucanpy.cli.base import BaseCommand
from boucanpy.db.models.user import User


class UserList(BaseCommand):
    name = "user-list"
    aliases = ["users"]
    description = "list users via DB"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        env = self.option("env")
        self.load_env(f"api.{env}")
        self.db_register()
        for user in self.session().query(User).all():
            print(user.id, user.email, user.is_superuser)
