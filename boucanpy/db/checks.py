from time import sleep
from boucanpy.core import logger
from boucanpy.db.session import session


def is_db_up():
    seconds = 0
    while True:
        if seconds > 60:
            logger.critical("could not start api. database not up")
            return False
        logger.debug("checking for db status")
        try:
            session().execute("SELECT 1")
            return True
        except KeyError as e:
            logger.critical(
                "database has not be registered. please call db_register(db_url)"
            )
            return False
        except Exception as e:
            logger.critical(
                "database check not ready after {} seconds: {}".format(
                    str(seconds), str(e.__class__.__name__)
                )
            )
        seconds = seconds + 1
        sleep(1)


def is_db_setup():
    seconds = 0
    while True:
        if seconds > 60:
            logger.critical("could not start api. database not setup")
            return False
        logger.debug("checking for db migrations")
        try:
            session().execute("SELECT * from alembic_version")
            return True
        except KeyError as e:
            logger.critical(
                "database has not be registered. please call db_register(db_url)"
            )
            return False
        except Exception as e:
            logger.critical(
                "database has not been migrated. please run: bdnsctl.py db-setup"
            )
            return False
        seconds = seconds + 1
        sleep(1)
