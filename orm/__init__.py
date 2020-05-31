from datetime import datetime
from itertools import chain
from typing import (
    TypeVar,
    Generic,
    Type,
    get_type_hints,
    Union,
    get_origin,
    get_args,
    Optional,
    List,
    Tuple, Callable, Set, Iterable
)

import aioredis
import redis
from aioredis.util import wait_ok

from orm.redis_set import RedisSet
from orm import redis_set

T = TypeVar('T')

client: aioredis.Redis
sync_client: redis.Redis


def connect(redis_client: aioredis.Redis):
    global client
    global sync_client
    client = redis_client
    sync_client = redis.Redis(
        unix_socket_path=client.address,
        decode_responses=True,
    )
    redis_set.client = client
    redis_set.sync_client = sync_client


class Table(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model: Type[T] = model
        self.name: str = model.__name__ + ':'
        self.counter_name: str = self.name + 'counter'
        self.redis_to_python = self.make_redis_to_python(model)
        self.model_has_id = hasattr(model, 'id')
        self.sets_description = self.make_sets_description(model)

    @classmethod
    def make_sets_description(cls, model: Type[T]) -> List[str]:
        return [
            key
            for key, type in get_type_hints(model).items()
            if cls.simplify_type(type) is set
        ]

    @classmethod
    def make_redis_to_python(cls, model: Type[T]) -> List[Tuple[str, Callable]]:
        return [
            (key, cls.simplify_type(type))
            for key, type in get_type_hints(model).items()
            if key != 'id'
        ]

    @classmethod
    def make_python_to_redis(cls, model: Type[T]) -> List[Tuple[str, Callable]]:
        return [
            (key, cls.simplify_type(type))
            for key, type in get_type_hints(model).items()
            if key != 'id'
        ]

    @classmethod
    def simplify_type(cls, complex_type: Type) -> Type:
        origin = get_origin(complex_type)
        args = get_args(complex_type)
        if origin is Union:
            if len(args) != 2 or args[1] is not type(None):
                raise TypeError("Union doesn't make sense")
            plain_type = cls.simplify_type(args[0])
        else:
            plain_type = origin
        if plain_type is datetime:
            plain_type = set
        return plain_type

    async def get(self, id: int) -> T:
        d = await client.hgetall(f'{self.name}{id}')
        if not d:
            raise IndexError

        obj = self.model.__new__(self.model)
        obj.__dict__ = {
            key: type(value) if (value := d.get(key)) is not None else None
            for key, type in self.redis_to_python
        }

        if self.model_has_id:
            obj.id = id

        for set_name in self.sets_description:
            setattr(obj, set_name, RedisSet(f'{self.name}{id}:{set_name}'))

        return obj

    async def save(self, obj: T, id: Optional[int] = None):
        if id is None:
            id = getattr(obj, 'id', None)
            if id is None:
                id = await client.incr(self.counter_name)

        if self.model_has_id:
            obj.id = id

        for set_name in self.sets_description:
            setattr(obj, set_name, RedisSet(f'{self.name}{id}:{set_name}'))

        d = ((key, str(value)) for key, value in obj.__dict__.items() if value is not None and key != 'id')
        return await wait_ok(client.execute(
            b'HMSET',
            f'{self.name}{id}',
            *chain.from_iterable(d)),
        )

    def get_set(self, id: int, name: str) -> RedisSet:
        return RedisSet(f'{self.name}{id}:{name}')
