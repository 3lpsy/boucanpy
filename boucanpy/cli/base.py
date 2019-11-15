from sys import exit
from os import environ
from typing import List

from boucanpy.core import (
    set_log_level,
    make_logger,
    set_log_format,
    get_uvicorn_logging,
    logger,
)
from boucanpy.core.security import create_bearer_token
from boucanpy.db.session import db_register, session
from boucanpy.db.utils import make_db_url


class BaseCommand:
    name = ""
    aliases = []
    description = ""
    add_log_level = False
    add_debug = False

    def __init__(self, options):
        self.options = self._args_to_dict(options)

    async def run(self):
        raise NotImplementedError()

    @classmethod
    def make(cls, args):
        # convert namespace to dict if not dict
        return cls(cls._args_to_dict(args))

    @classmethod
    def parser(cls, parser):
        if not cls.name:
            raise NotImplementedError()
        return parser

    async def call(self):
        if self.add_log_level:
            self.configure_logging()
        return await self.run()

    @classmethod
    def apply_parser(cls, sub_parser):
        parser = sub_parser.add_parser(
            cls.name, aliases=cls.aliases, help=cls.description
        )
        parser.add_argument(
            "-E", "--env", action="store", default="dev", help="environment"
        )
        if cls.add_log_level:
            parser.add_argument(
                "-L", "--log-level", action="store", default="info", help="log level"
            )
            parser.add_argument(
                "-F",
                "--log-format",
                action="store",
                default="full",
                choices=["full", "short"],
                help="log format",
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

    def configure_logging(self):
        set_log_level(self.get_log_level(), self.get_second_log_level())
        set_log_format(self.get_log_format())

    def get_uvicorn_logging(self):
        return get_uvicorn_logging(
            self.get_log_level(), self.get_second_log_level(), self.get_log_format()
        )

    def get_log_level(self):
        level = "info"
        second_level = level
        if self.option("log_level", None):
            level = self.option("log_level")
        elif self.option("debug", None):
            level = "debug"
        elif self.env("LOG_LEVEL", "info"):
            level = "info"
        return level

    def get_log_format(self):
        format_ = "FULL"
        if self.option("log_format", None):
            format_ = self.option("log_format").upper()
        return format_

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

    def env(self, key, default=None, int_=False):
        val = environ.get(key, default)
        if int_:
            return int(val)
        return val

    @classmethod
    def db_register(cls):
        return db_register(make_db_url())

    @classmethod
    def session(cls):
        return session()

    def exit(self, status):
        exit(status)

    @classmethod
    def _args_to_dict(self, options):
        return dict(vars(options)) if not isinstance(options, dict) else options
