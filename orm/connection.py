from typing import Optional

import aioredis
import redis

client: Optional[aioredis.Redis] = None
sync_client: Optional[redis.Redis] = None


def connect(redis_client: aioredis.Redis):
    global client
    global sync_client
    client = redis_client
    sync_client = redis.Redis(
        unix_socket_path=client.address,
        decode_responses=True,
    )