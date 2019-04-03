import aioredis
from .utils import make_broadcast_url


async def make_redis():
    return aioredis.create_redis(make_broadcast_url())


async def pubsub():
    pool = await make_redis()

    async def reader(channel):
        while await channel.wait_message():
            msg = await channel.get(encoding="utf-8")
            # ... process message ...
            print("message in {}: {}".format(channel.name, msg))

            if msg == STOPWORD:
                return

    with await pool as conn:
        await conn.execute_pubsub("subscribe", "channel:1")
        channel = conn.pubsub_channels["channel:1"]
        await reader(channel)  # wait for reader to complete
        await conn.execute_pubsub("unsubscribe", "channel:1")

    # Explicit connection usage
    conn = await pool.acquire()

    try:
        await conn.execute_pubsub("subscribe", "channel:1")
        channel = conn.pubsub_channels["channel:1"]
        await reader(channel)  # wait for reader to complete
        await conn.execute_pubsub("unsubscribe", "channel:1")
    finally:
        pool.release(conn)

    pool.close()
    await pool.wait_closed()
