import os

# late import of alembic because it destroys loggers
def initialize(directory=None, multidb=False):
    from alembic import command
    from alembic.config import Config as AlembicConfig

    class Config(AlembicConfig):
        def get_template_directory(self):
            package_dir = os.path.abspath(os.path.dirname(__file__))

            return os.path.join(package_dir, "templates")

    """Creates a new migration repository"""
    config = Config()
    config.set_main_option("script_location", directory)
    config.config_file_name = os.path.join(directory, "alembic.ini")
    command.init(config, directory, "singledb")
