import asyncio

import aioredis

from models import Author, authors, books, Book
from orm import connect


async def go():
    redis = await aioredis.create_redis_pool('/tmp/redis.sock', encoding='utf-8')
    connect(redis)

    print(list(await authors.search('Терри')))

    redis.close()
    await redis.wait_closed()

asyncio.run(go())



