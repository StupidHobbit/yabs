import asyncio

from models import Author, authors
from scripts.database_import.common import go


class AuthorsImporter:
    keys_mapping = {
        'FirstName': 'first_name',
        'MiddleName': 'middle_name',
        'LastName': 'last_name',
        'Nickname': 'nickname',
        'uid': 'uid',
        'Email': 'email',
        'Homepage': 'homepage',
        'Gender': 'gender',
        'MasterId': 'master_id',
        'AvtorId': 'id',
    }
    table_name = 'libavtorname'
    filters = None
    order = None
    join = ''

    async def process_row(self, row):
        d = {
            key: value
            for key, value in zip(self.keys_mapping.values(), row)
            if value or key.endswith('_name')
        }
        author = Author(**d)
        await authors.delete(author.id)
        await authors.save(author)


if __name__ == '__main__':
    asyncio.run(go(AuthorsImporter()))
