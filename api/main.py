import asyncio
from typing import List

import aioredis
from fastapi import FastAPI

from orm import connect
from api.authors.search import search_authors, SearchAuthors

app = FastAPI(title='Yabs', redoc_url=None)


@app.on_event("startup")
async def startup():
    # TODO use retry or something
    for _ in range(3):
        try:
            redis = await aioredis.create_redis_pool('/tmp/redis.sock')
        except aioredis.errors.ReplyError as e:
            await asyncio.sleep(10)
        else:
            break
    else:
        raise e
    connect(redis)


app.add_api_route('/search/authors', search_authors, response_model=List[SearchAuthors])
