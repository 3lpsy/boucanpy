import pytest
from boucanpy.cli.base import BaseCommand
from boucanpy.core.utils import test_dir, storage_dir
from boucanpy.core.utils import setenv


class Test(BaseCommand):
    name = "test"
    aliases = ["tests"]
    description = "run tests"

    @classmethod
    def parser(cls, parser):
        return parser

    async def run(self):
        self.db_register()
        setenv("API_DB_DATABASE", storage_dir("tmp"))
        print(test_dir("api"))
        pytest.main(["-x", test_dir("api")])
