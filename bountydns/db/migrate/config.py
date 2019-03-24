import os
import argparse
from alembic.config import Config as AlembicConfig


class Config(AlembicConfig):
    def get_template_directory(self):
        package_dir = os.path.abspath(os.path.dirname(__file__))

        return os.path.join(package_dir, "templates")


def get_config(directory, x_arg=None, opts=None):
    config = Config(os.path.join(directory, "alembic.ini"))
    config.set_main_option("script_location", directory)
    if config.cmd_opts is None:
        config.cmd_opts = argparse.Namespace()
    for opt in opts or []:
        setattr(config.cmd_opts, opt, True)
    if not hasattr(config.cmd_opts, "x"):
        if x_arg is not None:
            setattr(config.cmd_opts, "x", [])
            if isinstance(x_arg, list) or isinstance(x_arg, tuple):
                for x in x_arg:
                    config.cmd_opts.x.append(x)
            else:
                config.cmd_opts.x.append(x_arg)
        else:
            setattr(config.cmd_opts, "x", None)
    return config
