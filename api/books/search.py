from typing import Iterable

from pydantic import BaseModel
from redisearch import Query

from models import books
from orm import Table


class SearchBooks(BaseModel):
    id: int
    title: str


books_for_search = Table(SearchBooks, origin=books)


async def search_books(text: str) -> Iterable[SearchBooks]:
    query = Query(text).paging(0, 20)
    return await books_for_search.search(query)
