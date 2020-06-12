from typing import Set, Iterator, Iterable, TypeVar

from .connection import sync_client

T = TypeVar('T')


class RedisSet(Set[T]):
    def __init__(self, name) -> None:
        self.name = name

    def add(self, element: T) -> None:
        sync_client.sadd(self.name, element)

    def clear(self) -> None:
        sync_client.delete(self.name)

    def copy(self) -> Set[T]:
        raise NotImplementedError

    def difference(self, *s: 'RedisSet') -> Set[T]:
        return sync_client.sdiff(self.name, *[s.name for s in s])

    def difference_update(self, *s: 'RedisSet') -> None:
        sync_client.sdiffstore(self.name, self.name, *[s.name for s in s])

    def discard(self, element: T) -> None:
        sync_client.srem(self.name, element)

    def intersection(self, *s: 'RedisSet') -> Set[T]:
        return sync_client.sinter(self.name, *[s.name for s in s])

    def intersection_update(self, *s: 'RedisSet') -> None:
        sync_client.sinterstore(self.name, self.name, *[s.name for s in s])

    def isdisjoint(self, s: 'RedisSet') -> bool:
        return bool(sync_client.sinter(self.name, *[s.name for s in s]))

    def issubset(self, s: 'RedisSet') -> bool:
        raise NotImplementedError

    def issuperset(self, s: 'RedisSet') -> bool:
        raise NotImplementedError

    def pop(self) -> T:
        value = sync_client.spop(self.name)
        if value is None:
            raise KeyError
        return value

    def remove(self, element: T) -> None:
        deleted = sync_client.srem(self.name)
        if deleted == 0:
            raise KeyError

    def symmetric_difference(self, s: 'RedisSet') -> Set[T]:
        raise NotImplementedError

    def symmetric_difference_update(self, s: 'RedisSet') -> None:
        raise NotImplementedError

    def union(self, *s: 'RedisSet') -> Set[T]:
        return sync_client.sunion(self.name, *[s.name for s in s])

    def update(self, *s: Iterable[T]) -> None:
        sync_client.sadd(self.name, *s)

    def __len__(self) -> int:
        return sync_client.scard(self.name)

    def __contains__(self, o: object) -> bool:
        return sync_client.sismember(self.name, o)

    def __iter__(self) -> Iterator[T]:
        return iter(sync_client.smembers(self.name))

    def __str__(self) -> str:
        return str(sync_client.smembers(self.name))
