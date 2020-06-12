import asyncio

import aioredis
from fastapi import FastAPI

from models import authors
from orm import connect


async def setup():
    redis = await aioredis.create_redis_pool('/tmp/redis.sock')
    connect(redis)


app = FastAPI(on_startup=[setup])


@app.get("/search/authors")
async def search_authors(text: str):
    return await authors.search(text)
