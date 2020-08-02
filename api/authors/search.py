from typing import Iterable

from pydantic import BaseModel
from redisearch import Query

from models import authors
from orm import Table


class SearchAuthors(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str


authors_for_search = Table(SearchAuthors, origin=authors)


async def search_authors(text: str) -> Iterable[SearchAuthors]:
    query = Query(text).paging(0, 20)
    return await authors_for_search.search(query)
