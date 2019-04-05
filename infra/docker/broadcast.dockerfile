FROM redis

ENV REDIS_PASSWORD=redis
COPY redis.conf /usr/local/etc/redis/redis.conf

WORKDIR /data

CMD ["sh", "-c", "exec redis-server /usr/local/etc/redis/redis.conf --requirepass \"$REDIS_PASSWORD\""]
