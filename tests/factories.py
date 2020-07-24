from dataclasses import field, dataclass

from faker import Faker
from faker.providers import person

from models import Author, authors
from orm import Table, T


fake = Faker()
fake.add_provider(person)


class Factory(Table[T]):
    async def create(self, *args, **kwargs) -> T:
        obj = self.model(*args, **kwargs)
        await self.save(obj)
        return obj


@dataclass
class AuthorFactory(Author):
    first_name: str = field(default_factory=fake.first_name)
    middle_name: str = ''
    last_name: str = field(default_factory=fake.last_name)


authors = Factory(AuthorFactory, origin=authors)
