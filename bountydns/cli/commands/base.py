from sys import exit
from bountydns.core import load_env, set_log_level, make_logger
from bountydns.core.security import create_bearer_token
from bountydns.db.session import db_register, session
from bountydns.db.utils import make_db_url


class BaseCommand:
    name = ""
    aliases = []
    description = ""
    add_log_level = False
    add_debug = False

    def __init__(self, options):
        self.options = options

    async def run(self):
        raise NotImplementedError()

    @classmethod
    def make(cls, args):
        # convert namespace to dict if not dict
        options = dict(vars(args)) if not isinstance(args, dict) else args
        return cls(options)

    @classmethod
    def parser(cls, parser):
        if not cls.name:
            raise NotImplementedError()
        return parser

    async def call(self):
        if self.add_log_level:
            set_log_level(self.get_log_level(), self.get_second_log_level())
        return await self.run()

    @classmethod
    def apply_parser(cls, sub_parser):
        parser = sub_parser.add_parser(
            cls.name, aliases=cls.aliases, help=cls.description
        )
        if cls.add_log_level:
            parser.add_argument(
                "-L", "--log-level", action="store", default="info", help="log level"
            )
            parser.add_argument(
                "--second-log-level",
                action="store",
                default="info",
                help="secondary log level",
            )

            parser.add_argument(
                "--no-envs", action="store_true", help="don't load env files"
            )
        if cls.add_debug:
            parser.add_argument("-D", "--debug", action="store_true", help="debug")

        return cls.parser(parser)

    def get_log_level(self):
        level = "info"
        second_level = level
        if self.option("debug", None):
            level = "debug"
        elif self.option("log_level", None):
            level = self.option("log_level")
        return level

    def get_second_log_level(self):
        if self.option("second_log_level", None):
            second_level = self.option("second_log_level")
        elif self.option("debug", None):
            second_level = "debug"
        else:
            second_level = self.get_log_level()
        return second_level

    @classmethod
    def has_command(cls, command):
        return command in [cls.name] + cls.aliases

    def option(self, key, default="dne"):
        if default == "dne":
            return self.options.get(key)
        return self.options.get(key, default)

    def set_option(self, key, val):
        self.options[key] = val
        return self

    def load_env(self, *args):
        if not self.option("no_envs", False):
            for key in args:
                load_env(key)
            return True
        return False

    @classmethod
    def db_register(cls):
        return db_register(make_db_url())

    @classmethod
    def session(cls):
        return session()

    def exit(self, status):
        exit(status)
