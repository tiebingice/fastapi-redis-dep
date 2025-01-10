from typing import Sequence

from redis.asyncio import Redis

SetVal = str | bytes | int | float



class RedisSet:
    def __init__(self, client: Redis):
        self._client = client

    async def add(self, key: str, *members: SetVal) -> int:
        return await self._client.sadd(key, *members)

    async def remove(self, key: str, *members: SetVal) -> int:
        return await self._client.srem(key, *members)

    async def exists(self, key: str, member: SetVal) -> int:
        return await self._client.sismember(key, member) > 0

    async def get_all(self, key: str) -> set[SetVal]:
        members = await self._client.smembers(key)
        return set(members)

    async def length(self, key: str) -> int:
        return await self._client.scard(key)

    async def intersection(self, keys: Sequence[str]) -> set[SetVal]:
        return set(await self._client.sinter(*keys))

    async def union(self, keys: Sequence[str]) -> set[SetVal]:
        return set(await self._client.sunion(*keys))

    async def difference(self, keys: Sequence[str]) -> set[SetVal]:
        return set(await self._client.sdiff(*keys))
