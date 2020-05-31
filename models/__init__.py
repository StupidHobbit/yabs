from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

from orm import Table


@dataclass
class Author:
    first_name: str
    middle_name: str
    last_name: str
    books: Set[int] = field(default_factory=set)
    nickname: Optional[str] = None
    uid: Optional[int] = None
    email: Optional[str] = None
    homepage: Optional[str] = None
    gender: Optional[str] = None
    master_id: Optional[id] = None
    id: Optional[int] = None


@dataclass
class Book:
    file_size: int
    time: datetime
    title: str
    language: str
    file_type: str
    tags: str = ''
    authors: Set[int] = field(default_factory=set)
    encoding: Optional[str] = None
    additional_title: Optional[str] = None
    source_language: Optional[str] = None
    year: Optional[int] = None
    chars: Optional[int] = None
    pages: Optional[int] = None
    id: Optional[int] = None


authors = Table(Author)
books = Table(Book)
