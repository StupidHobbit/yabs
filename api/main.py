import asyncio
from typing import List

import aioredis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from orm import connect, GetError
from api.authors import search_authors, SearchAuthors
from api.books import search_books, SearchBooks, get_book, Book

app = FastAPI(title='Yabs', redoc_url=None)


@app.exception_handler(GetError)
async def unicorn_exception_handler(request: Request, exc: GetError):
    return JSONResponse(
        status_code=404,
        content={'message': f'Object "{exc.table.model.__name__}" with id = {id} does not exist'},
    )


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
app.add_api_route('/search/books', search_books, response_model=List[SearchBooks])
app.add_api_route('/books/{id}', get_book, response_model=Book)
