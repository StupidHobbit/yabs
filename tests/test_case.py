from unittest import IsolatedAsyncioTestCase

import aioredis

from orm import connect


class DatabaseTestCase(IsolatedAsyncioTestCase):
    redis = None

    async def asyncSetUp(self) -> None:
        if self.redis is None:
            type(self).redis = await aioredis.create_redis_pool('/tmp/redis-test.sock', encoding='utf-8')
        connect(self.redis)

    async def asyncTearDown(self) -> None:
        await self.redis.flushall()
