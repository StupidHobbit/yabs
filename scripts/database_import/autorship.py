import asyncio

from models import books, authors
from scripts.database_import.common import go


class AuthorshipImporter:
    keys_mapping = {
        'AvtorId': '',
        'BookId': '',
    }
    table_name = 'libavtor'
    filters = {
        'Deleted': 0,
    }
    order = ''
    join = 'JOIN libbook ON libavtor.BookId = libbook.BookId'

    async def process_row(self, row):
        author, book = row
        authors.get_set(author, 'books').add(book)
        books.get_set(book, 'authors').add(author)


if __name__ == '__main__':
    asyncio.run(go(AuthorshipImporter()))
