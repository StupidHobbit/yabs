import asyncio
from datetime import datetime

import aioredis

from models import Author, authors, books, Book
from orm import connect


async def go():
    redis = await aioredis.create_redis_pool('/tmp/redis.sock', encoding='utf-8')
    connect(redis)

    await books.save(Book(file_size=1, time=datetime.now(), id=1))
    print(await books.get(1))

    redis.close()
    await redis.wait_closed()

asyncio.run(go())



