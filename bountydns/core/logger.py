import logging
import alembic

# TODO: this doesn't work, fix it
# TODO: Fix this nonsense

LIB_LOGGERS = [
    "alembic.runtime.migration",
    "alembic.env",
    "alembic.autogenerate.compare",
]


def make_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
    )

    logger = logging.getLogger("dnsserver")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger, handler


logger, handler = make_logger()


def get_logger():
    return logger


def get_handler():
    return handler


def set_log_level(level, second_level=None):
    second_level = second_level or level
    get_logger().info(f"setting log levels to {level} and {second_level}")
    get_logger().setLevel(getattr(logging, level.upper()))
    get_handler().setLevel(getattr(logging, level.upper()))

    for l in LIB_LOGGERS:

        sl = logging.getLogger(l)
        sl.setLevel(getattr(logging, second_level.upper()))
