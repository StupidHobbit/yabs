from fastapi.testclient import TestClient

from api.main import app
from api.books import search_books
from tests import factories
from tests.test_case import DatabaseTestCase

client = TestClient(app)


class BooksTestCase(DatabaseTestCase):
    async def test_search(self):
        book = await factories.books.create()
        await factories.books.create()

        search_result = list(await search_books(book.title))
        self.assertEqual(len(search_result), 1)
        self.assertDictEqual(
            search_result[0].dict(),
            {
                'id': book.id,
                'title': book.title,
            },
        )
