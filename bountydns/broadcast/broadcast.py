import aioredis
from .utils import make_broadcast_url

publisher = None


async def make_redis():
    return await aioredis.create_redis(make_broadcast_url())


async def make_subscriber(name):
    subscriber = await make_redis()
    res = await subscriber.subscribe(f"channel:{name}")
    channel = res[0]
    return subscriber, channel


# can't create_redis outside of async ?
