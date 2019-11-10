import logging
import alembic
from os import environ

# TODO: this doesn't work, fix it
# TODO: Fix this nonsense

## for second log level
## useful for quieting noisy loggers
LIB_LOGGERS = [
    # "aioredis",
    # "alembic",
    "alembic.runtime",
    "alembic.runtime.ddl",
    "alembic.ddl.postgresql",
    "alembic.runtime.migration",
    "alembic.env",
    "alembic.autogenerate",
    "alembic.autogenerate.compare",
    # "alembic.util",
    # "alembic.util.messaging",
    # "asyncio",
    "passlib",
    "passlib.ifc",
    "passlib.context",
    "passlib.registry",
    "passlib.utils",
    "passlib.utils.compat",
    "passlib.utils.binary",
    "passlib.utils.handlers",
    "passlib.utils.decor",
    "passlib.handlers",
    "passlib.handlers.bcrypt",
    # "sqlalchemy",
    # "sqlalchemy.query",
    # "sqlalchemy.ext",
    # "sqlalchemy.ext.baked",
    # "sqlalchemy.orm",
    # "sqlalchemy.orm.mapper",
    # "sqlalchemy.orm.properties",
    # "sqlalchemy.orm.dynamic",
    # "sqlalchemy.orm.strategies",
    # "sqlalchemy.orm.relationships",
    # "sqlalchemy.pool",
    # "sqlalchemy.pool.impl",
    # "sqlalchemy.engine",
    # "sqlalchemy.engine.base",
    # "sqlalchemy.dialects",
    # "sqlalchemy.dialects.postgresql"
    # "elasticsearch",
    # "elasticsearch.trace",
    # "fastapi",
    "faker",
    "faker.factory",
    "factory",
    "factory.generate",
    # "passlib",
    # "uvicorn",
    # "uvicorn.error",
    # "uvicorn.access",
    # "uvicorn.asgi",
    "websockets",
    "websockets.client",
    "websockets.server",
    "websockets.protocol",
]

## place in api.py to see loggerts to uvicorn runtime
## place in cli to see loggers at cli time
# import logging
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# for l in loggers:
#     print(l)


def make_logger():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    log_level = environ.get("LOG_LEVEL", "INFO").upper()
    log_format = environ.get("LOG_FORMAT", "FULL").upper()
    if log_format == "VERBOSE" or log_format == "FULL":
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%H:%M:%S",
            )
        )
    else:
        handler.setFormatter(
            logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        )

    level = getattr(logging, log_level, "INFO")
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("make_logger@.logger.py - Logger built")
    return logger, handler


logger, handler = make_logger()

# TODO: are these unecessary?
def get_logger():
    global logger
    return logger


def get_handler():
    global handler
    return handler


def set_log_format(format_="FULL"):
    get_logger().debug(f"set_log_format@.logger.py - Setting log format to {format_}")

    if format_ == "VERBOSE" or format_ == "FULL":
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S",
        )
    else:
        formatter = logging.Formatter("%(levelname)s - %(message)s")

    get_handler().setFormatter(formatter)
    get_logger().debug("set_log_format@.logger.py - Root Logger level set")

    if format_ == "VERBOSE" or format_ == "FULL":
        lib_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S",
        )
    else:
        lib_formatter = logging.Formatter("%(levelname)s - %(message)s")

    get_logger().debug(
        f"set_log_format@.logger.py - Setting log format to {format_} for library loggers"
    )

    for l in LIB_LOGGERS:
        sl = logging.getLogger(l)
        for h in sl.handlers:
            h.setFormatter(lib_formatter)


def set_log_level(level, second_level=None):
    second_level = second_level or level
    get_logger().debug(
        f"set_log_level@.logger.py - setting log levels to {level} and {second_level}"
    )
    get_logger().setLevel(getattr(logging, level.upper(), "INFO"))
    get_handler().setLevel(getattr(logging, level.upper(), "INFO"))

    get_logger().debug("set_log_level@.logger.py - Root Logger level set")

    get_logger().info(
        f"set_log_level@.logger.py - Setting library logger level to {second_level.upper()}"
    )

    for l in LIB_LOGGERS:
        sl = logging.getLogger(l)
        sl.setLevel(getattr(logging, second_level.upper(), "WARNING"))


# Any changes made to the logger are lost when uvicorn takes over
# Use this config to get a similar logging experience in uvicorn
def get_uvicorn_logging(level, second_level, format_):
    if format_ == "VERBOSE" or format_ == "FULL":
        uvicorn_default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        uvicorn_access_format = '%(levelname)s - default@uvicorn - client:%(client_addr)s - request:"%(request_line)s" status:%(status_code)s'
    else:
        uvicorn_default_format = "%(levelname)s - %(message)s"
        uvicorn_access_format = (
            '%(levelname)s - access@uvicorn - "%(request_line)s" %(status_code)s'
        )

    if hasattr(logging, level.upper()):
        level = level.upper()
    else:
        level = "INFO"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": uvicorn_default_format,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": uvicorn_access_format,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": level},
            "uvicorn.error": {"level": level},
            "uvicorn.access": {
                "handlers": ["access"],
                "level": level,
                "propagate": False,
            },
        },
    }

    if hasattr(logging, second_level.upper()):
        second_level = second_level.upper()
    else:
        second_level = "WARNING"

    for l in LIB_LOGGERS:
        if l not in logging_config["loggers"].keys():
            logging_config["loggers"][l] = {
                "level": second_level,
            }
    return logging_config
