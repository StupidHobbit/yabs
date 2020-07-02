import aioredis
from fastapi import FastAPI

from orm import connect


async def setup():
    import api.urls

    redis = await aioredis.create_redis_pool('/tmp/redis.sock')
    connect(redis)


app = FastAPI(on_startup=[setup])
