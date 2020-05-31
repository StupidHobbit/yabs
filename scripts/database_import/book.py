import asyncio

from models import Book, books
from scripts.database_import.common import go


class BooksImporter:
    keys_mapping = {
        'FileSize': 'file_size',
        'Time': 'time',
        'Title': 'title',
        'Lang': 'language',
        'FileType': 'file_type',
        'Keywords': 'tags',
        'Encoding': 'encoding',
        'Title1': 'additional_title',
        'SrcLang': 'source_language',
        'Year': 'year',
        'Chars': 'chars',
        'Pages': 'pages',
        'BookId': 'id',
    }
    table_name = 'libbook'
    filters = {
        'Deleted': 0,
    }
    order = None
    join = ''

    async def process_row(self, row):
        d = {
            key: value
            for key, value in zip(self.keys_mapping.values(), row)
            if value or key in ['tags', 'language']
        }
        book = Book(**d)
        await books.save(book)


if __name__ == '__main__':
    asyncio.run(go(BooksImporter()))
