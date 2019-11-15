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
        self.db_register()
        for user in self.session().query(User).all():
            print(user.id, user.email, user.is_superuser)
