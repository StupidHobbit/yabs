from typing import Protocol, Dict, Tuple, Any, Optional, Iterable

import aioredis
from tqdm import tqdm
import aiomysql

from orm import connect


class Importer(Protocol):
    keys_mapping: Dict[str, str]
    table_name: str
    filters: Optional[Dict[str, Any]]
    order: Optional[Iterable[str]]
    join: str

    async def process_row(self, row: Tuple): ...


async def go(importer: Importer):
    connection = await aiomysql.connect(
        user='hobbit',
        password='1234',
        db='library',
        charset='utf8mb4',
    )

    redis = await aioredis.create_redis_pool('/tmp/redis.sock')
    connect(redis)

    where_str = 'WHERE ' + " ".join(
        f"{key} = {value}"
        for key, value in importer.filters.items()
    ) if importer.filters is not None else ''

    async with connection.cursor() as cursor:
        await cursor.execute(
            f'SELECT COUNT(*) '
            f'FROM {importer.table_name} '
            f'{importer.join} '            
            f'{where_str};')
        total, = await cursor.fetchone()

    async with connection.cursor() as cursor:
        await cursor.execute(
            f'SELECT {", ".join(importer.keys_mapping)} '
            f'FROM {importer.table_name} '
            f'{importer.join} '            
            f'{where_str} '
            f'{importer.order};'
        )

        with tqdm(total=total, desc='Importing') as progress:
            async for row in cursor:
                await importer.process_row(row)
                progress.update()
