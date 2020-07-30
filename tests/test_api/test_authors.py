from fastapi.testclient import TestClient

from api.main import app
from api.authors import search_authors
from tests import factories
from tests.test_case import DatabaseTestCase

client = TestClient(app)


class AuthorsTestCase(DatabaseTestCase):
    async def test_search(self):
        author = await factories.authors.create()
        await factories.authors.create()

        search_result = list(await search_authors(f'{author.first_name} '
                                                  f'{author.last_name}'))
        self.assertEqual(len(search_result), 1)
        self.assertDictEqual(
            search_result[0].dict(),
            {
                'id': author.id,
                'first_name': author.first_name,
                'middle_name': author.middle_name,
                'last_name': author.last_name,
            },
        )
