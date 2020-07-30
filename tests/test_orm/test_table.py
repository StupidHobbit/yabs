from dataclasses import dataclass

from orm import Table
from tests.test_case import DatabaseTestCase


class AuthorsTestCase(DatabaseTestCase):
    async def test_get_save_get_simple(self):
        @dataclass
        class Model:
            a: int

        table = Table(Model)
        m = Model(a=2)
        id = await table.save(m)

        self.assertEqual(await table.get(id), m)
