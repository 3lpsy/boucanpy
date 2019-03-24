import os
from alembic import command
from bountydns.db.migrate.config import Config


def initialize(directory=None, multidb=False):
    """Creates a new migration repository"""
    config = Config()
    config.set_main_option("script_location", directory)
    config.config_file_name = os.path.join(directory, "alembic.ini")
    command.init(config, directory, "singledb")
