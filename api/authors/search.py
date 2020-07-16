from typing import List

from pydantic import BaseModel
from redisearch import Query

from models import authors
from orm import Table
from fastapi import APIRouter


class SearchAuthors(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str


authors_for_search = Table(SearchAuthors, origin=authors)

router = APIRouter()


@router.get("/search/authors", response_model=List[SearchAuthors])
async def search_authors(text: str):
    query = Query(text).paging(0, 20)
    return await authors_for_search.search(query)
