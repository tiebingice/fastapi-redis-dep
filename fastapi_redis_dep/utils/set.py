from typing import Sequence, cast,Awaitable,TypeAlias

from redis.asyncio import Redis

SetType: TypeAlias = str| bytes | int| float

class RedisSet:
    def __init__(self, client: Redis):
        self._client: Redis = client

    async def add(self, key: str, *members: SetType) -> bool:
        return await cast(Awaitable[int], self._client.sadd(key, *members))==1

    async def remove(self, key: str, *members: SetType) -> bool:
        return await cast(Awaitable[int], self._client.srem(key, *members))==1

    async def exists(self, key: str, member: SetType) -> bool:
        return await cast(Awaitable[int], self._client.sismember(key, str(member)))==1


    async def get_all(self, key: str) -> set[SetType]:
        members = await cast(Awaitable[set[SetType]], self._client.smembers(key))
        return members


    async def length(self, key: str) -> int:
        return await cast(Awaitable[int], self._client.scard(key))

    async def intersection(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Awaitable[list[SetType]], self._client.sinter(list(keys))))


    async def union(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Awaitable[list[SetType]], self._client.sunion(list(keys))))


    async def difference(self, keys: Sequence[str]) -> set[SetType]:
        return set(await cast(Awaitable[list[SetType]], self._client.sdiff(list(keys))))
