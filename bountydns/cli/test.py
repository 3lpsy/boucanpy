import pytest
from bountydns.cli.base import BaseCommand
from bountydns.core.utils import test_dir, storage_dir
from bountydns.core.utils import setenv


class Test(BaseCommand):
    name = "test"
    aliases = ["tests"]
    description = "run tests"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        self.load_env("api.test")
        self.load_env("db.test")
        self.db_register()
        setenv("API_DB_DATABASE", storage_dir("tmp"))
        print(test_dir("api"))
        pytest.main(["-x", test_dir("api")])
