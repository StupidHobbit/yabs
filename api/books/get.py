from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from orm import Table
import models


@dataclass
class Book(models.Book):
    pass


books = Table(Book, origin=models.books)


async def get_book(id: int) -> Book:
    return await books.get(id)
