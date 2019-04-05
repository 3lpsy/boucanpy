from time import sleep
from bountydns.core import logger
from bountydns.broadcast import make_redis


async def is_broadcast_up():
    seconds = 0
    while True:
        if seconds > 60:
            logger.critical("could not start api. broadcast (queue) not up")
            return False
        logger.debug("checking for broadcast (queue) status")
        try:
            redis = await make_redis()
            await redis.set("up-key", "value")
            val = await redis.get("up-key")
            val = await redis.delete("up-key")
            return True
        except Exception as e:
            logger.critical(
                "broadcast (queue) check not ready after {} seconds: {}".format(
                    str(seconds), str(e.__class__.__name__)
                )
            )
        seconds = seconds + 2
        sleep(2)
