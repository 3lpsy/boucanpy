from boucanpy.core.utils import getenv

# TODO: no caps


def make_broadcast_url():
    BROADCAST_USER = ""
    BROADCAST_DRIVER = getenv("BROADCAST_DRIVER", "redis")
    BROADCAST_PATH = getenv("BROADCAST_PATH", "0")
    BROADCAST_HOST = getenv("BROADCAST_HOST", "broadcast")
    BROADCAST_PORT = getenv("BROADCAST_PORT", "6379")
    BROADCAST_PASSWORD = getenv("BROADCAST_PASSWORD", "broadcast")
    BROADCAST_URL = f"{BROADCAST_DRIVER}://{BROADCAST_USER}:{BROADCAST_PASSWORD}@{BROADCAST_HOST}:{BROADCAST_PORT}/{BROADCAST_PATH}"

    return BROADCAST_URL
