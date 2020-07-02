from typing import List

from pydantic import BaseModel
from redisearch import Query

from api.main import app
from models import authors
from orm import Table


class SearchAuthors(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str


authors_for_search = Table(SearchAuthors, origin=authors)


@app.get("/search/authors", response_model=List[SearchAuthors])
async def search_authors(text: str):
    query = Query(text).paging(0, 20)
    return await authors_for_search.search(query)
