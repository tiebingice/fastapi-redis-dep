from typing import Any, cast

from redis.asyncio import Redis


ZSetValue = str| bytes| int| float
ZSetMember =str| bytes


class RedisZset:
    def __init__(self, client: Redis):
        self._client: Redis = client

    async def add(self, key: str, members_with_scores: dict[ZSetMember, ZSetValue]) -> int:
        return await cast(Any, self._client).zadd(key, members_with_scores)

    async def remove(self, key: str, *members: ZSetMember) -> int:
        return await cast(Any, self._client).zrem(key, *members)

    async def score(self, key: str, member: ZSetMember) -> float | None:
        return await cast(Any, self._client).zscore(key, member)

    async def get_all(self, key: str, start: int = 0, stop: int = -1, withscores: bool = False) -> list[
        tuple[str, float] | str]:
        members = await cast(Any, self._client).zrange(key, start, stop, withscores=withscores)
        if withscores:
            return [(str(member), score) for member, score in members]
        return [str(member) for member in members]

    async def length(self, key: str) -> int:
        return await cast(Any, self._client).zcard(key)

    async def range_by_score(self, key: str, min_: float, max_: float, start: int = 0, num: int = 5,
                             withscores: bool = False) -> list[str | tuple[str, float]]:

        members = await cast(Any, self._client).zrangebyscore(key, min_, max_, start=start, num=num,
                                                             withscores=withscores)

        if withscores:
            return [(str(member), score) for member, score in members]
        return [str(member) for member in members]

    async def rank(self, key: str, member: ZSetMember, reverse: bool = False) -> int:
        if reverse:
            return await cast(Any, self._client).zrevrank(key, member)
        else:
            return await cast(Any, self._client).zrank(key, member)
