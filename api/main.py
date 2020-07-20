import aioredis
from fastapi import FastAPI

from orm import connect
from api.authors.search import router as authors

async def setup():
    redis = await aioredis.create_redis_pool('redis://redis:6379')
    connect(redis)


app = FastAPI(on_startup=[setup], title='Yabs', redoc_url=None)
app.include_router(authors)
