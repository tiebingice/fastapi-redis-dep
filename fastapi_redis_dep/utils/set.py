from typing import Sequence, Any, cast

from redis.asyncio import Redis

SetType = str| bytes| int|float

class RedisSet:
    def __init__(self, client: Redis):
        self._client: Redis = client

    async def add(self, key: str, *members: SetType) -> int:
        return await cast(Any, self._client).sadd(key, *members)

    async def remove(self, key: str, *members: SetType) -> int:
        return await cast(Any, self._client).srem(key, *members)

    async def exists(self, key: str, member: SetType) -> bool:
        return await cast(Any, self._client).sismember(key, member)

    async def get_all(self, key: str) -> set[SetType]:
        members = await cast(Any, self._client).smembers(key)
        return set(members)

    async def length(self, key: str) -> int:
        return await cast(Any, self._client).scard(key)

    async def intersection(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Any, self._client).sinter(*keys))

    async def union(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Any, self._client).sunion(*keys))

    async def difference(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Any, self._client).sdiff(*keys))
